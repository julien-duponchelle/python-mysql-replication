import struct

from .constants import FIELD_TYPE


class Column(object):
    """Definition of a column"""

    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            self.__parse_column_definition(*args)
        else:
            self.__dict__.update(kwargs)

    def __parse_column_definition(self, column_type, packet):
        self.type = column_type
        self.name = None
        self.unsigned = False
        self.is_primary = False
        self.charset_id = None
        self.character_set_name = None
        self.collation_name = None
        self.enum_values = None
        self.set_values = None
        self.visibility = False

        if self.type == FIELD_TYPE.VARCHAR:
            self.max_length = struct.unpack("<H", packet.read(2))[0]
        elif self.type == FIELD_TYPE.DOUBLE:
            self.size = packet.read_uint8()
        elif self.type == FIELD_TYPE.FLOAT:
            self.size = packet.read_uint8()
        elif self.type == FIELD_TYPE.TIMESTAMP2:
            self.fsp = packet.read_uint8()
        elif self.type == FIELD_TYPE.DATETIME2:
            self.fsp = packet.read_uint8()
        elif self.type == FIELD_TYPE.TIME2:
            self.fsp = packet.read_uint8()
        elif self.type == FIELD_TYPE.VAR_STRING or self.type == FIELD_TYPE.STRING:
            self.__read_string_metadata(packet)
        elif self.type == FIELD_TYPE.BLOB:
            self.length_size = packet.read_uint8()
        elif self.type == FIELD_TYPE.GEOMETRY:
            self.length_size = packet.read_uint8()
        elif self.type == FIELD_TYPE.JSON:
            self.length_size = packet.read_uint8()
        elif self.type == FIELD_TYPE.NEWDECIMAL:
            self.precision = packet.read_uint8()
            self.decimals = packet.read_uint8()
        elif self.type == FIELD_TYPE.BIT:
            bits = packet.read_uint8()
            bytes = packet.read_uint8()
            self.bits = (bytes * 8) + bits
            self.bytes = int((self.bits + 7) / 8)

    def __read_string_metadata(self, packet):
        metadata = (packet.read_uint8() << 8) + packet.read_uint8()
        real_type = metadata >> 8
        if real_type == FIELD_TYPE.SET or real_type == FIELD_TYPE.ENUM:
            self.type = real_type
            self.size = metadata & 0x00FF
        else:
            self.max_length = (((metadata >> 4) & 0x300) ^ 0x300) + (metadata & 0x00FF)

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return not self.__eq__(other)

    def serializable_data(self):
        return self.data

    @property
    def data(self):
        return dict((k, v) for (k, v) in self.__dict__.items() if not k.startswith("_"))
