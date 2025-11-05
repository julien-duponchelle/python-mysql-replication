import struct
import decimal
import datetime
import logging

from pymysql.charset import charset_by_name
from enum import Enum

from .event import BinLogEvent
from .constants import FIELD_TYPE
from .constants import BINLOG
from .constants import CHARSET
from .constants import NONE_SOURCE
from .column import Column
from .table import Table
from .bitmap import BitCount, BitGet



# MySQL 5.7 compatibility: Cache for INFORMATION_SCHEMA column names
_COLUMN_NAME_CACHE = {}

class RowsEvent(BinLogEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super().__init__(from_packet, event_size, table_map, ctl_connection, **kwargs)
        self.__rows = None
        self.__only_tables = kwargs["only_tables"]
        self.__ignored_tables = kwargs["ignored_tables"]
        self.__only_schemas = kwargs["only_schemas"]
        self.__ignored_schemas = kwargs["ignored_schemas"]
        self.__none_sources = {}

        # Header
        self.table_id = self._read_table_id()

        # Additional information
        try:
            self.primary_key = table_map[self.table_id].data["primary_key"]
            self.schema = self.table_map[self.table_id].schema
            self.table = self.table_map[self.table_id].table
        except KeyError:  # If we have filter the corresponding TableMap Event
            self._processed = False
            return

        if self.__only_tables is not None and self.table not in self.__only_tables:
            self._processed = False
            return
        elif self.__ignored_tables is not None and self.table in self.__ignored_tables:
            self._processed = False
            return

        if self.__only_schemas is not None and self.schema not in self.__only_schemas:
            self._processed = False
            return
        elif (
            self.__ignored_schemas is not None and self.schema in self.__ignored_schemas
        ):
            self._processed = False
            return

        # Event V2
        if (
            self.event_type == BINLOG.WRITE_ROWS_EVENT_V2
            or self.event_type == BINLOG.DELETE_ROWS_EVENT_V2
            or self.event_type == BINLOG.UPDATE_ROWS_EVENT_V2
            or self.event_type == BINLOG.PARTIAL_UPDATE_ROWS_EVENT
        ):
            self.flags, self.extra_data_length = struct.unpack(
                "<HH", self.packet.read(4)
            )
            if self.extra_data_length > 2:
                self.extra_data_type = struct.unpack("<B", self.packet.read(1))[0]
                # ndb information
                if self.extra_data_type == 0:
                    self.nbd_info_length, self.nbd_info_format = struct.unpack(
                        "<BB", self.packet.read(2)
                    )
                    self.nbd_info = self.packet.read(self.nbd_info_length - 2)
                # partition information
                elif self.extra_data_type == 1:
                    if (
                        self.event_type == BINLOG.UPDATE_ROWS_EVENT_V2
                        or self.event_type == BINLOG.PARTIAL_UPDATE_ROWS_EVENT
                    ):
                        self.partition_id, self.source_partition_id = struct.unpack(
                            "<HH", self.packet.read(4)
                        )
                    else:
                        self.partition_id = struct.unpack("<H", self.packet.read(2))[0]

                # etc
                else:
                    self.extra_data = self.packet.read(self.extra_data_length - 3)
        else:
            self.flags = struct.unpack("<H", self.packet.read(2))[0]

        # Body
        self.number_of_columns = self.packet.read_length_coded_binary()
        self.columns = self.table_map[self.table_id].columns

    @staticmethod
    def _is_null(null_bitmap, position):
        bit = null_bitmap[int(position / 8)]
        if isinstance(bit, str):
            bit = ord(bit)
        return bit & (1 << (position % 8))

    def _read_column_data(self, cols_bitmap, row_image_type=None):
        """Use for WRITE, UPDATE and DELETE events.
        Return an array of column data
        """
        self.is_partial_json_update = False
        partial_bitmap = None
        if (
            self.event_type == BINLOG.PARTIAL_UPDATE_ROWS_EVENT
            and row_image_type == RowImageType.UpdateAI
        ):
            binlog_row_value_option = self.packet.read_length_coded_binary()
            self.is_partial_json_update = binlog_row_value_option & 0b10000001 != 0
            if self.is_partial_json_update:
                partial_bitmap = self.packet.read((self._json_column_count() + 7) / 8)
        values = {}

        # null bitmap length = (bits set in 'columns-present-bitmap'+7)/8
        # See http://dev.mysql.com/doc/internals/en/rows-event.html
        null_bitmap = self.packet.read((BitCount(cols_bitmap) + 7) / 8)

        null_bitmap_index = 0
        partial_bitmap_index = 0
        nb_columns = len(self.columns)
        for i in range(0, nb_columns):
            is_partial = False
            column = self.columns[i]
            name = self.table_map[self.table_id].columns[i].name
            unsigned = self.table_map[self.table_id].columns[i].unsigned

            if (
                self.is_partial_json_update
                and row_image_type == RowImageType.UpdateAI
                and column.type == FIELD_TYPE.JSON
            ):
                if BitGet(partial_bitmap, partial_bitmap_index) > 0:
                    is_partial = True
                partial_bitmap_index += 1

            if not name:
                # If you are using mysql 5.7 or mysql 8, but binlog_row_metadata = "MINIMAL",
                # we do not know the column information.
                # If you know column information,
                # mysql 5.7 version Users Use Under 1.0 version
                # mysql 8.0 version Users Set binlog_row_metadata = "FULL"
                name = "UNKNOWN_COL" + str(i)
            values[name] = self.__read_values_name(
                column,
                null_bitmap,
                null_bitmap_index,
                is_partial,
                cols_bitmap,
                unsigned,
                i,
            )

            if BitGet(cols_bitmap, i) != 0:
                null_bitmap_index += 1

        return values

    def __read_values_name(
        self,
        column,
        null_bitmap,
        null_bitmap_index,
        is_partial,
        cols_bitmap,
        unsigned,
        i,
    ):
        name = self.table_map[self.table_id].columns[i].name
        if BitGet(cols_bitmap, i) == 0:
            # This block is only executed when binlog_row_image = MINIMAL.
            # When binlog_row_image = FULL, this block does not execute.
            self.__none_sources[name] = NONE_SOURCE.COLS_BITMAP
            return None

        if self._is_null(null_bitmap, null_bitmap_index):
            self.__none_sources[name] = NONE_SOURCE.NULL
            return None

        if column.type == FIELD_TYPE.TINY:
            if unsigned:
                ret = struct.unpack("<B", self.packet.read(1))[0]
                return ret
            else:
                return struct.unpack("<b", self.packet.read(1))[0]
        elif column.type == FIELD_TYPE.SHORT:
            if unsigned:
                ret = struct.unpack("<H", self.packet.read(2))[0]
                return ret
            else:
                return struct.unpack("<h", self.packet.read(2))[0]
        elif column.type == FIELD_TYPE.LONG:
            if unsigned:
                ret = struct.unpack("<I", self.packet.read(4))[0]
                return ret
            else:
                return struct.unpack("<i", self.packet.read(4))[0]
        elif column.type == FIELD_TYPE.INT24:
            if unsigned:
                ret = self.packet.read_uint24()
                return ret
            else:
                return self.packet.read_int24()
        elif column.type == FIELD_TYPE.FLOAT:
            return struct.unpack("<f", self.packet.read(4))[0]
        elif column.type == FIELD_TYPE.DOUBLE:
            return struct.unpack("<d", self.packet.read(8))[0]
        elif column.type == FIELD_TYPE.VARCHAR or column.type == FIELD_TYPE.STRING:
            ret = (
                self.__read_string(2, column)
                if column.max_length > 255
                else self.__read_string(1, column)
            )

            return ret
        elif column.type == FIELD_TYPE.NEWDECIMAL:
            return self.__read_new_decimal(column)
        elif column.type == FIELD_TYPE.BLOB:
            return self.__read_string(column.length_size, column)
        elif column.type == FIELD_TYPE.DATETIME:
            ret = self.__read_datetime()
            if ret is None:
                self.__none_sources[name] = NONE_SOURCE.OUT_OF_DATETIME_RANGE
            return ret
        elif column.type == FIELD_TYPE.TIME:
            return self.__read_time()
        elif column.type == FIELD_TYPE.DATE:
            ret = self.__read_date()
            if ret is None:
                self.__none_sources[name] = NONE_SOURCE.OUT_OF_DATE_RANGE
            return ret
        elif column.type == FIELD_TYPE.TIMESTAMP:
            return datetime.datetime.utcfromtimestamp(self.packet.read_uint32())

        # For new date format:
        elif column.type == FIELD_TYPE.DATETIME2:
            ret = self.__read_datetime2(column)
            if ret is None:
                self.__none_sources[name] = NONE_SOURCE.OUT_OF_DATETIME2_RANGE
            return ret
        elif column.type == FIELD_TYPE.TIME2:
            return self.__read_time2(column)
        elif column.type == FIELD_TYPE.TIMESTAMP2:
            return self.__add_fsp_to_time(
                datetime.datetime.utcfromtimestamp(self.packet.read_int_be_by_size(4)),
                column,
            )
        elif column.type == FIELD_TYPE.LONGLONG:
            if unsigned:
                ret = self.packet.read_uint64()
                return ret
            else:
                return self.packet.read_int64()
        elif column.type == FIELD_TYPE.YEAR:
            return self.packet.read_uint8() + 1900
        elif column.type == FIELD_TYPE.ENUM:
            if column.enum_values:
                return column.enum_values[self.packet.read_uint_by_size(column.size)]
            self.packet.read_uint_by_size(column.size)
            return None
        elif column.type == FIELD_TYPE.SET:
            bit_mask = self.packet.read_uint_by_size(column.size)
            if column.set_values:
                ret = {
                    val
                    for idx, val in enumerate(column.set_values)
                    if bit_mask & (1 << idx)
                }
                if not ret:
                    self.__none_sources[column.name] = NONE_SOURCE.EMPTY_SET
                    return None
                return ret
            self.__none_sources[column.name] = NONE_SOURCE.EMPTY_SET
            return None
        elif column.type == FIELD_TYPE.BIT:
            return self.__read_bit(column)
        elif column.type == FIELD_TYPE.GEOMETRY:
            return self.packet.read_length_coded_pascal_string(column.length_size)
        elif column.type == FIELD_TYPE.JSON:
            value = self.packet.read_binary_json(column.length_size, is_partial)
            if not value and is_partial:
                self.__none_sources[column.name] = NONE_SOURCE.JSON_PARTIAL_UPDATE
            return value
        else:
            raise NotImplementedError(f"Unknown MySQL column type: {column.type}")

    def __add_fsp_to_time(self, time, column):
        """Read and add the fractional part of time
        For more details about new date format:
        http://dev.mysql.com/doc/internals/en/date-and-time-data-type-representation.html
        """
        microsecond = self.__read_fsp(column)
        if microsecond > 0:
            time = time.replace(microsecond=microsecond)
        return time

    def __read_fsp(self, column):
        read = 0
        if column.fsp == 1 or column.fsp == 2:
            read = 1
        elif column.fsp == 3 or column.fsp == 4:
            read = 2
        elif column.fsp == 5 or column.fsp == 6:
            read = 3
        if read > 0:
            microsecond = self.packet.read_int_be_by_size(read)
            if column.fsp % 2:
                microsecond = int(microsecond / 10)
            return microsecond * (10 ** (6 - column.fsp))
        return 0

    @staticmethod
    def charset_to_encoding(name):
        charset = charset_by_name(name)
        return charset.encoding if charset else name

    def __read_string(self, size, column):
        string = self.packet.read_length_coded_pascal_string(size)
        origin_string = string
        decode_errors = "ignore" if self._ignore_decode_errors else "strict"
        if column.character_set_name is not None:
            encoding = self.charset_to_encoding(column.character_set_name)
            try:
                string = string.decode(encoding, decode_errors)
            except LookupError:
                # python does not support Mysql encoding type ex)swe7 it will not decoding then Show origin string
                string = origin_string
        else:
            # MYSQL 5.xx Version  Goes Here
            # We don't know encoding type So apply Default Utf-8
            string = string.decode(errors=decode_errors)
        return string

    def __read_bit(self, column):
        """Read MySQL BIT type"""
        resp = ""
        for byte in range(0, column.bytes):
            current_byte = ""
            data = self.packet.read_uint8()
            if byte == 0:
                if column.bytes == 1:
                    end = column.bits
                else:
                    end = column.bits % 8
                    if end == 0:
                        end = 8
            else:
                end = 8
            for bit in range(0, end):
                if data & (1 << bit):
                    current_byte += "1"
                else:
                    current_byte += "0"
            resp += current_byte[::-1]
        return resp

    def __read_time(self):
        time = self.packet.read_uint24()
        date = datetime.timedelta(
            hours=int(time / 10000),
            minutes=int((time % 10000) / 100),
            seconds=int(time % 100),
        )
        return date

    def __read_time2(self, column):
        """TIME encoding for nonfractional part:

         1 bit sign    (1= non-negative, 0= negative)
         1 bit unused  (reserved for future extensions)
        10 bits hour   (0-838)
         6 bits minute (0-59)
         6 bits second (0-59)
        ---------------------
        24 bits = 3 bytes
        """
        data = self.packet.read_int_be_by_size(3)

        sign = 1 if self.__read_binary_slice(data, 0, 1, 24) else -1
        if sign == -1:
            # negative integers are stored as 2's compliment
            # hence take 2's compliment again to get the right value.
            data = ~data + 1

        t = (
            datetime.timedelta(
                hours=self.__read_binary_slice(data, 2, 10, 24),
                minutes=self.__read_binary_slice(data, 12, 6, 24),
                seconds=self.__read_binary_slice(data, 18, 6, 24),
                microseconds=self.__read_fsp(column),
            )
            * sign
        )
        return t

    def __read_date(self):
        time = self.packet.read_uint24()
        if time == 0:  # nasty mysql 0000-00-00 dates
            return None

        year = (time & ((1 << 15) - 1) << 9) >> 9
        month = (time & ((1 << 4) - 1) << 5) >> 5
        day = time & ((1 << 5) - 1)
        if year == 0 or month == 0 or day == 0:
            return None

        date = datetime.date(year=year, month=month, day=day)
        return date

    def __read_datetime(self):
        value = self.packet.read_uint64()
        if value == 0:  # nasty mysql 0000-00-00 dates
            return None

        date = value / 1000000
        time = int(value % 1000000)

        year = int(date / 10000)
        month = int((date % 10000) / 100)
        day = int(date % 100)
        if year == 0 or month == 0 or day == 0:
            return None

        date = datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=int(time / 10000),
            minute=int((time % 10000) / 100),
            second=int(time % 100),
        )
        return date

    def __read_datetime2(self, column):
        """DATETIME

        1 bit  sign           (1= non-negative, 0= negative)
        17 bits year*13+month  (year 0-9999, month 0-12)
         5 bits day            (0-31)
         5 bits hour           (0-23)
         6 bits minute         (0-59)
         6 bits second         (0-59)
        ---------------------------
        40 bits = 5 bytes
        """
        data = self.packet.read_int_be_by_size(5)
        year_month = self.__read_binary_slice(data, 1, 17, 40)
        try:
            t = datetime.datetime(
                year=int(year_month / 13),
                month=year_month % 13,
                day=self.__read_binary_slice(data, 18, 5, 40),
                hour=self.__read_binary_slice(data, 23, 5, 40),
                minute=self.__read_binary_slice(data, 28, 6, 40),
                second=self.__read_binary_slice(data, 34, 6, 40),
            )
        except ValueError:
            self.__read_fsp(column)
            return None
        return self.__add_fsp_to_time(t, column)

    def __read_new_decimal(self, column):
        """Read MySQL's new decimal format introduced in MySQL 5"""

        # This project was a great source of inspiration for
        # understanding this storage format.
        # https://github.com/jeremycole/mysql_binlog

        digits_per_integer = 9
        compressed_bytes = [0, 1, 1, 2, 2, 3, 3, 4, 4, 4]
        integral = column.precision - column.decimals
        uncomp_integral = int(integral / digits_per_integer)
        uncomp_fractional = int(column.decimals / digits_per_integer)
        comp_integral = integral - (uncomp_integral * digits_per_integer)
        comp_fractional = column.decimals - (uncomp_fractional * digits_per_integer)

        # Support negative
        # The sign is encoded in the high bit of the the byte
        # But this bit can also be used in the value
        value = self.packet.read_uint8()
        if value & 0x80 != 0:
            res = ""
            mask = 0
        else:
            mask = -1
            res = "-"
        self.packet.unread(struct.pack("<B", value ^ 0x80))

        size = compressed_bytes[comp_integral]
        if size > 0:
            value = self.packet.read_int_be_by_size(size) ^ mask
            res += str(value)

        for i in range(0, uncomp_integral):
            value = struct.unpack(">i", self.packet.read(4))[0] ^ mask
            res += f"{value:09d}"

        res += "."

        for i in range(0, uncomp_fractional):
            value = struct.unpack(">i", self.packet.read(4))[0] ^ mask
            res += f"{value:09d}"

        size = compressed_bytes[comp_fractional]
        if size > 0:
            value = self.packet.read_int_be_by_size(size) ^ mask
            res += f"{value:0{comp_fractional}d}"

        return decimal.Decimal(res)

    def __read_binary_slice(self, binary, start, size, data_length):
        """
        Read a part of binary data and extract a number
        binary: the data
        start: From which bit (1 to X)
        size: How many bits should be read
        data_length: data size
        """
        binary = binary >> data_length - (start + size)
        mask = (1 << size) - 1
        return binary & mask

    def _json_column_count(self):
        count = 0
        for column in self.columns:
            if column.type == FIELD_TYPE.JSON:
                count += 1
        return count

    def _get_none_sources(self, column_data):
        result = {}
        for column_name, value in column_data.items():
            if (column_name is None) or (value is not None):
                continue

            source = self.__none_sources.get(column_name, "null")
            result[column_name] = source
        return result

    def _dump(self):
        super()._dump()
        print(f"Table: {self.schema}.{self.table}")
        print(f"Affected columns: {self.number_of_columns}")
        print(f"Changed rows: {len(self.rows)}")
        print(
            f"Column Name Information Flag: {self.table_map[self.table_id].column_name_flag}"
        )

    def _fetch_rows(self):
        self.__rows = []

        if not self.complete:
            return

        while self.packet.read_bytes < self.event_size:
            self.__rows.append(self._fetch_one_row())

    @property
    def rows(self):
        if self.__rows is None:
            self._fetch_rows()
        return self.__rows


class DeleteRowsEvent(RowsEvent):
    """This event is trigger when a row in the database is removed

    For each row you have a hash with a single key: values which contain the data of the removed line.
    """

    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super().__init__(from_packet, event_size, table_map, ctl_connection, **kwargs)
        if self._processed:
            self.columns_present_bitmap = self.packet.read(
                (self.number_of_columns + 7) / 8
            )

    def _fetch_one_row(self):
        row = {}

        row["values"] = self._read_column_data(self.columns_present_bitmap)
        row["none_sources"] = self._get_none_sources(row["values"])

        return row

    def _dump(self):
        super()._dump()
        print("Values:")
        for row in self.rows:
            print("--")
            for key in row["values"]:
                none_source = (
                    row["none_sources"][key] if key in row["none_sources"] else ""
                )
                if none_source:
                    print(f"* {key} : {row['values'][key]} ({none_source})")
                else:
                    print(f"* {key} : {row['values'][key]}")


class WriteRowsEvent(RowsEvent):
    """This event is triggered when a row in database is added

    For each row you have a hash with a single key: values which contain the data of the new line.
    """

    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super().__init__(from_packet, event_size, table_map, ctl_connection, **kwargs)
        if self._processed:
            self.columns_present_bitmap = self.packet.read(
                (self.number_of_columns + 7) / 8
            )

    def _fetch_one_row(self):
        row = {}

        row["values"] = self._read_column_data(self.columns_present_bitmap)
        row["none_sources"] = self._get_none_sources(row["values"])

        return row

    def _dump(self):
        super()._dump()
        print("Values:")
        for row in self.rows:
            print("--")
            for key in row["values"]:
                none_source = (
                    row["none_sources"][key] if key in row["none_sources"] else ""
                )
                if none_source:
                    print(f"* {key} : {row['values'][key]} ({none_source})")
                else:
                    print(f"* {key} : {row['values'][key]}")


class UpdateRowsEvent(RowsEvent):
    """This event is triggered when a row in the database is changed

    For each row you got a hash with two keys:
        * before_values
        * after_values

    Depending of your MySQL configuration the hash can contains the full row or only the changes:
    http://dev.mysql.com/doc/refman/5.6/en/replication-options-binary-log.html#sysvar_binlog_row_image
    """

    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super().__init__(from_packet, event_size, table_map, ctl_connection, **kwargs)

        if self._processed:
            # Body
            self.columns_present_bitmap = self.packet.read(
                (self.number_of_columns + 7) / 8
            )
            self.columns_present_bitmap2 = self.packet.read(
                (self.number_of_columns + 7) / 8
            )

    def _fetch_one_row(self):
        row = {}

        row["before_values"] = self._read_column_data(self.columns_present_bitmap)
        row["before_none_sources"] = self._get_none_sources(row["before_values"])
        row["after_values"] = self._read_column_data(self.columns_present_bitmap2)
        row["after_none_sources"] = self._get_none_sources(row["after_values"])
        return row

    def _dump(self):
        super()._dump()
        print("Values:")
        for row in self.rows:
            print("--")
            for key in row["before_values"]:
                if key in row["before_none_sources"]:
                    before_value_info = (
                        f'{row["before_values"][key]} ',
                        f'{row["before_none_sources"][key]} ',
                    )
                else:
                    before_value_info = row["before_values"][key]

                if key in row["after_none_sources"]:
                    after_value_info = (
                        f'{row["after_values"][key]} ',
                        f'{row["after_none_sources"][key]} ',
                    )
                else:
                    after_value_info = row["after_values"][key]

                print(f"*{key}:{before_value_info}=>{after_value_info}")


class OptionalMetaData:
    def __init__(self):
        self.unsigned_column_list = []
        self.default_charset_collation = None
        self.charset_collation = {}
        self.column_charset = []
        self.column_name_list = []
        self.set_str_value_list = []
        self.set_enum_str_value_list = []
        self.geometry_type_list = []
        self.simple_primary_key_list = []
        self.primary_keys_with_prefix = {}
        self.enum_and_set_default_charset = None
        self.enum_and_set_charset_collation = {}
        self.enum_and_set_default_column_charset_list = []
        self.charset_collation_list = []
        self.enum_and_set_collation_list = []
        self.visibility_list = []

    def dump(self):
        print(f"=== {self.__class__.__name__} ===")
        print(f"unsigned_column_list: {self.unsigned_column_list}")
        print(f"default_charset_collation: {self.default_charset_collation}")
        print(f"charset_collation: {self.charset_collation}")
        print(f"column_charset: {self.column_charset}")
        print(f"column_name_list: {self.column_name_list}")
        print(f"set_str_value_list : {self.set_str_value_list}")
        print(f"set_enum_str_value_list : {self.set_enum_str_value_list}")
        print(f"geometry_type_list : {self.geometry_type_list}")
        print(f"simple_primary_key_list: {self.simple_primary_key_list}")
        print(f"primary_keys_with_prefix: {self.primary_keys_with_prefix}")
        print(f"visibility_list: {self.visibility_list}")
        print(f"charset_collation_list: {self.charset_collation_list}")
        print(f"enum_and_set_collation_list: {self.enum_and_set_collation_list}")


class TableMapEvent(BinLogEvent):
    """This event describes the structure of a table.
    It's sent before a change happens on a table.
    An end user of the lib should have no usage of this
    """

    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super().__init__(from_packet, event_size, table_map, ctl_connection, **kwargs)

        self.__only_tables = kwargs["only_tables"]
        self.__ignored_tables = kwargs["ignored_tables"]
        self.__only_schemas = kwargs["only_schemas"]
        self.__ignored_schemas = kwargs["ignored_schemas"]
        self.__freeze_schema = kwargs["freeze_schema"]
        self.__optional_meta_data = kwargs["optional_meta_data"]
        self.__enable_logging = kwargs.get("enable_logging", False)
        self.__use_column_name_cache = kwargs.get("use_column_name_cache", False)
        # Post-Header
        self.table_id = self._read_table_id()

        if self.table_id in table_map and self.__freeze_schema:
            self._processed = False
            return

        self.flags = struct.unpack("<H", self.packet.read(2))[0]

        # Payload
        self.schema_length = struct.unpack("!B", self.packet.read(1))[0]
        self.schema = self.packet.read(self.schema_length).decode()
        self.packet.advance(1)
        self.table_length = struct.unpack("!B", self.packet.read(1))[0]
        self.table = self.packet.read(self.table_length).decode()

        if self.__only_tables is not None and self.table not in self.__only_tables:
            self._processed = False
            return
        elif self.__ignored_tables is not None and self.table in self.__ignored_tables:
            self._processed = False
            return

        if self.__only_schemas is not None and self.schema not in self.__only_schemas:
            self._processed = False
            return
        elif (
            self.__ignored_schemas is not None and self.schema in self.__ignored_schemas
        ):
            self._processed = False
            return

        self.packet.advance(1)
        self.column_count = self.packet.read_length_coded_binary()

        self.columns = []
        self.dbms = self.dbms or self._ctl_connection._get_dbms()
        # Read columns meta data
        column_types = bytearray(self.packet.read(self.column_count))
        self.packet.read_length_coded_binary()
        for i in range(0, len(column_types)):
            column_type = column_types[i]
            col = Column(column_type, from_packet)
            self.columns.append(col)

        # ith column is nullable if (i - 1)th bit is set to True, not nullable otherwise
        ## Refer to definition of and call to row.event._is_null() to interpret bitmap corresponding to columns
        self.null_bitmask = self.packet.read((self.column_count + 7) / 8)
        self.table_obj = Table(self.table_id, self.schema, self.table, self.columns)
        table_map[self.table_id] = self.table_obj
        self.optional_metadata = self._get_optional_meta_data()
        self._sync_column_info()

    def get_table(self):
        return self.table_obj

    def _dump(self):
        super()._dump()
        print(f"Table id: {self.table_id}")
        print(f"Schema: {self.schema}")
        print(f"Table: {self.table}")
        print(f"Columns: {self.column_count}")
        if self.__optional_meta_data:
            self.optional_metadata.dump()

    def _get_optional_meta_data(self):
        """
        DEFAULT_CHARSET and COLUMN_CHARSET don't appear together,
        and ENUM_AND_SET_DEFAULT_CHARSET and ENUM_AND_SET_COLUMN_CHARSET don't appear together.
        They are just alternative ways to pack character set information.
        When binlogging, it logs character sets in the way that occupies least storage.

        TLV format data (TYPE, LENGTH, VALUE)
        """
        optional_metadata = OptionalMetaData()
        while self.packet.bytes_to_read() > BINLOG.BINLOG_CHECKSUM_LEN:
            option_metadata_type = self.packet.read(1)[0]
            length = self.packet.read_length_coded_binary()

            field_type: MetadataFieldType = MetadataFieldType.by_index(
                option_metadata_type
            )

            if field_type == MetadataFieldType.SIGNEDNESS:
                signed_column_list = self._convert_include_non_numeric_column(
                    self._read_bool_list(length, True)
                )
                optional_metadata.unsigned_column_list = signed_column_list

            elif field_type == MetadataFieldType.DEFAULT_CHARSET:
                (
                    optional_metadata.default_charset_collation,
                    optional_metadata.charset_collation,
                ) = self._read_default_charset(length)
                optional_metadata.charset_collation_list = (
                    self._parsed_column_charset_by_default_charset(
                        optional_metadata.default_charset_collation,
                        optional_metadata.charset_collation,
                        self._is_character_column,
                    )
                )

            elif field_type == MetadataFieldType.COLUMN_CHARSET:
                optional_metadata.column_charset = self._read_ints(length)
                optional_metadata.charset_collation_list = (
                    self._parsed_column_charset_by_column_charset(
                        optional_metadata.column_charset, self._is_character_column
                    )
                )

            elif field_type == MetadataFieldType.COLUMN_NAME:
                optional_metadata.column_name_list = self._read_column_names(length)

            elif field_type == MetadataFieldType.SET_STR_VALUE:
                optional_metadata.set_str_value_list = self._read_type_values(length)

            elif field_type == MetadataFieldType.ENUM_STR_VALUE:
                optional_metadata.set_enum_str_value_list = self._read_type_values(
                    length
                )

            elif field_type == MetadataFieldType.GEOMETRY_TYPE:
                optional_metadata.geometry_type_list = self._read_ints(length)

            elif field_type == MetadataFieldType.SIMPLE_PRIMARY_KEY:
                optional_metadata.simple_primary_key_list = self._read_ints(length)

            elif field_type == MetadataFieldType.PRIMARY_KEY_WITH_PREFIX:
                optional_metadata.primary_keys_with_prefix = (
                    self._read_primary_keys_with_prefix(length)
                )

            elif field_type == MetadataFieldType.ENUM_AND_SET_DEFAULT_CHARSET:
                (
                    optional_metadata.enum_and_set_default_charset,
                    optional_metadata.enum_and_set_charset_collation,
                ) = self._read_default_charset(length)

                optional_metadata.enum_and_set_collation_list = (
                    self._parsed_column_charset_by_default_charset(
                        optional_metadata.enum_and_set_default_charset,
                        optional_metadata.enum_and_set_charset_collation,
                        self._is_enum_or_set_column,
                    )
                )

            elif field_type == MetadataFieldType.ENUM_AND_SET_COLUMN_CHARSET:
                optional_metadata.enum_and_set_default_column_charset_list = (
                    self._read_ints(length)
                )

                optional_metadata.enum_and_set_collation_list = (
                    self._parsed_column_charset_by_column_charset(
                        optional_metadata.enum_and_set_default_column_charset_list,
                        self._is_enum_or_set_column,
                    )
                )

            elif field_type == MetadataFieldType.VISIBILITY:
                optional_metadata.visibility_list = self._read_bool_list(length, False)

        return optional_metadata


    def _fetch_column_names_from_schema(self):
        """
        Fetch column names from INFORMATION_SCHEMA for MySQL 5.7 compatibility.

        Only executes if use_column_name_cache=True is enabled.
        Uses module-level cache to avoid repeated queries.

        Returns:
            list: Column names in ORDINAL_POSITION order, or empty list
        """
        # Only fetch if explicitly enabled (opt-in feature)
        if not self.__use_column_name_cache:
            return []

        cache_key = f"{self.schema}.{self.table}"

        # Check cache first
        if cache_key in _COLUMN_NAME_CACHE:
            return _COLUMN_NAME_CACHE[cache_key]

        try:
            query = """
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """
            cursor = self._ctl_connection.cursor()
            cursor.execute(query, (self.schema, self.table))
            rows = cursor.fetchall()
            # Handle both tuple and dict cursor results
            if rows and isinstance(rows[0], dict):
                column_names = [row['COLUMN_NAME'] for row in rows]
            else:
                column_names = [row[0] for row in rows]
            cursor.close()

            # Cache result
            _COLUMN_NAME_CACHE[cache_key] = column_names

            if self.__enable_logging and column_names:
                logging.info(f"Cached column names for {cache_key}: {len(column_names)} columns")

            return column_names
        except Exception as e:
            if self.__enable_logging:
                logging.warning(f"Failed to fetch column names for {cache_key}: {type(e).__name__}: {e}")
            # Cache empty result to avoid retry spam
            _COLUMN_NAME_CACHE[cache_key] = []
            return []

    def _sync_column_info(self):
        if not self.__optional_meta_data:
            column_names = self._fetch_column_names_from_schema()
            if column_names and len(column_names) == self.column_count:
                for column_idx in range(self.column_count):
                    self.columns[column_idx].name = column_names[column_idx]
            return
        if len(self.optional_metadata.column_name_list) == 0:
            column_names = self._fetch_column_names_from_schema()
            if column_names and len(column_names) == self.column_count:
                for column_idx in range(self.column_count):
                    self.columns[column_idx].name = column_names[column_idx]
            return
        charset_pos = 0
        enum_or_set_pos = 0
        enum_pos = 0
        set_pos = 0

        for column_idx in range(self.column_count):
            column_type = self.columns[column_idx].type
            column_name = self.optional_metadata.column_name_list[column_idx]
            column_data: Column = self.columns[column_idx]
            column_data.name = column_name

            if self._is_character_column(column_type, dbms=self.dbms):
                charset_id = self.optional_metadata.charset_collation_list[charset_pos]
                charset_pos += 1
                encode_name, collation_name, charset_name = find_charset(
                    str(charset_id), dbms=self.dbms
                )
                self.columns[column_idx].collation_name = collation_name
                self.columns[column_idx].character_set_name = encode_name

            if self._is_enum_or_set_column(column_type):
                charset_id = self.optional_metadata.enum_and_set_collation_list[
                    enum_or_set_pos
                ]
                enum_or_set_pos += 1

                encode_name, collation_name, charset_name = find_charset(
                    str(charset_id), dbms=self.dbms
                )

                self.columns[column_idx].collation_name = collation_name
                self.columns[column_idx].character_set_name = encode_name

                if self._is_enum_column(column_type):
                    enum_column_info = self.optional_metadata.set_enum_str_value_list[
                        enum_pos
                    ]
                    self.columns[column_idx].enum_values = [""] + enum_column_info
                    enum_pos += 1

                if self._is_set_column(column_type):
                    set_column_info = self.optional_metadata.set_str_value_list[set_pos]
                    self.columns[column_idx].set_values = set_column_info
                    set_pos += 1

            if (
                self.optional_metadata.unsigned_column_list
                and self.optional_metadata.unsigned_column_list[column_idx]
            ):
                self.columns[column_idx].unsigned = True

            if column_idx in self.optional_metadata.simple_primary_key_list:
                self.columns[column_idx].is_primary = True

            if (
                self.optional_metadata.visibility_list
                and self.optional_metadata.visibility_list[column_idx]
            ):
                self.columns[column_idx].visibility = True

        self.table_obj = Table(
            self.table_id, self.schema, self.table, self.columns, column_name_flag=True
        )

    def _convert_include_non_numeric_column(self, signedness_bool_list):
        # The incoming order of columns in the packet represents the indices of the numeric columns.
        # Thus, it transforms non-numeric columns to align with the sorting.
        bool_list = []
        position = 0
        for i in range(self.column_count):
            column_type = self.columns[i].type
            if self._is_numeric_column(column_type):
                if signedness_bool_list[position]:
                    bool_list.append(True)
                else:
                    bool_list.append(False)
                position += 1
            else:
                bool_list.append(False)

        return bool_list

    def _parsed_column_charset_by_default_charset(
        self,
        default_charset_collation: int,
        column_charset_collation: dict,
        column_type_detect_function,
    ):
        column_charset = []
        position = 0
        for i in range(self.column_count):
            column_type = self.columns[i].type
            if not column_type_detect_function(column_type, dbms=self.dbms):
                continue
            else:
                if position not in column_charset_collation.keys():
                    column_charset.append(default_charset_collation)
                else:
                    column_charset.append(column_charset_collation[position])
                position += 1

        return column_charset

    def _parsed_column_charset_by_column_charset(
        self, column_charset_list: list, column_type_detect_function
    ):
        column_charset = []
        position = 0
        if len(column_charset_list) == 0:
            return
        for i in range(self.column_count):
            column_type = self.columns[i].type
            if not column_type_detect_function(column_type, dbms=self.dbms):
                continue
            else:
                column_charset.append(column_charset_list[position])
                position += 1

        return column_charset

    def _read_bool_list(self, read_byte_length, signedness_flag):
        # if signedness_flag true
        # The order of the index in the packet is only the index between the numeric_columns.
        # Therefore, we need to use numeric_column_count when calculating bits.
        bool_list = []
        bytes_data = self.packet.read(read_byte_length)

        byte = 0
        byte_idx = 0
        bit_idx = 0

        for i in range(self.column_count):
            column_type = self.columns[i].type
            if not self._is_numeric_column(column_type) and signedness_flag:
                continue
            if bit_idx == 0:
                byte = bytes_data[byte_idx]
                byte_idx += 1
            bool_list.append((byte & (0b10000000 >> bit_idx)) != 0)
            bit_idx = (bit_idx + 1) % 8
        return bool_list

    def _read_default_charset(self, length):
        charset = {}
        read_until = self.packet.read_bytes + length
        if self.packet.read_bytes >= read_until:
            return
        default_charset_collation = self.packet.read_length_coded_binary()
        while self.packet.read_bytes < read_until:
            column_index = self.packet.read_length_coded_binary()
            charset_collation = self.packet.read_length_coded_binary()
            charset[column_index] = charset_collation

        return default_charset_collation, charset

    def _read_ints(self, length):
        result = []
        read_until = self.packet.read_bytes + length
        while self.packet.read_bytes < read_until:
            result.append(self.packet.read_length_coded_binary())
        return result

    def _read_column_names(self, length):
        result = []
        read_until = self.packet.read_bytes + length
        while self.packet.read_bytes < read_until:
            result.append(self.packet.read_variable_length_string().decode())
        return result

    def _read_type_values(self, length):
        result = []
        read_until = self.packet.read_bytes + length
        if self.packet.read_bytes >= read_until:
            return
        while self.packet.read_bytes < read_until:
            type_value_list = []
            value_count = self.packet.read_length_coded_binary()
            for i in range(value_count):
                value = self.packet.read_variable_length_string()
                decode_value = ""
                try:
                    decode_value = value.decode()
                except UnicodeDecodeError:
                    # ignore not utf-8 decode type
                    pass
                type_value_list.append(decode_value)
            result.append(type_value_list)
        return result

    def _read_primary_keys_with_prefix(self, length):
        ints = self._read_ints(length)
        result = {}
        for i in range(0, len(ints), 2):
            result[ints[i]] = ints[i + 1]
        return result

    @staticmethod
    def _is_character_column(column_type, dbms="mysql"):
        if column_type in [
            FIELD_TYPE.STRING,
            FIELD_TYPE.VAR_STRING,
            FIELD_TYPE.VARCHAR,
            FIELD_TYPE.BLOB,
        ]:
            return True
        if column_type == FIELD_TYPE.GEOMETRY and dbms == "mariadb":
            return True
        return False

    @staticmethod
    def _is_enum_column(column_type):
        if column_type == FIELD_TYPE.ENUM:
            return True
        return False

    @staticmethod
    def _is_set_column(column_type):
        if column_type == FIELD_TYPE.SET:
            return True
        return False

    @staticmethod
    def _is_enum_or_set_column(column_type, dbms="mysql"):
        if column_type in [FIELD_TYPE.ENUM, FIELD_TYPE.SET]:
            return True
        return False

    @staticmethod
    def _is_numeric_column(column_type):
        if column_type in [
            FIELD_TYPE.TINY,
            FIELD_TYPE.SHORT,
            FIELD_TYPE.INT24,
            FIELD_TYPE.LONG,
            FIELD_TYPE.LONGLONG,
            FIELD_TYPE.NEWDECIMAL,
            FIELD_TYPE.FLOAT,
            FIELD_TYPE.DOUBLE,
            FIELD_TYPE.YEAR,
        ]:
            return True
        return False


class PartialUpdateRowsEvent(UpdateRowsEvent):
    def __init__(self, from_packet, event_size, table_map, ctl_connection, **kwargs):
        super().__init__(from_packet, event_size, table_map, ctl_connection, **kwargs)

    def _fetch_one_row(self):
        row = {}
        row_image_type = RowImageType.UpdateBI
        row["before_values"] = self._read_column_data(
            self.columns_present_bitmap, row_image_type
        )
        row["before_none_sources"] = self._get_none_sources(row["before_values"])
        row_image_type = RowImageType.UpdateAI
        row["after_values"] = self._read_column_data(
            self.columns_present_bitmap2, row_image_type
        )
        row["after_none_sources"] = self._get_none_sources(row["after_values"])

        return row

    def _dump(self):
        super()._dump()


def find_charset(charset_id, dbms="mysql"):
    encode = None
    collation_name = None
    charset_name = None
    charset: CHARSET.Charset = CHARSET.charset_by_id(charset_id, dbms)
    if charset is None:
        encode = "utf8"
        charset_name = "utf8"
    else:
        encode = charset.encoding
        collation_name = charset.collation
        charset_name = charset.name
    return encode, collation_name, charset_name


class MetadataFieldType(Enum):
    SIGNEDNESS = 1  # Signedness of numeric columns
    DEFAULT_CHARSET = 2  # Charsets of character columns
    COLUMN_CHARSET = 3  # Charsets of character columns
    COLUMN_NAME = 4  # Names of columns
    SET_STR_VALUE = 5  # The string values of SET columns
    ENUM_STR_VALUE = 6  # The string values in ENUM columns
    GEOMETRY_TYPE = 7  # The real type of geometry columns
    SIMPLE_PRIMARY_KEY = 8  # The primary key without any prefix
    PRIMARY_KEY_WITH_PREFIX = 9  # The primary key with some prefix
    ENUM_AND_SET_DEFAULT_CHARSET = 10  # Charsets of ENUM and SET columns
    ENUM_AND_SET_COLUMN_CHARSET = 11  # Charsets of ENUM and SET columns
    VISIBILITY = 12
    UNKNOWN_METADATA_FIELD_TYPE = 128

    @staticmethod
    def by_index(index):
        return MetadataFieldType(index)


class RowImageType(Enum):
    # https://github.com/mysql/mysql-server/blob/1bfe02bdad6604d54913c62614bde57a055c8332/sql/rpl_record.h#L39
    WriteAI = 0
    UpdateBI = 1
    UpdateAI = 2
    DeleteBI = 3

    @staticmethod
    def by_index(index):
        return RowImageType(index)
