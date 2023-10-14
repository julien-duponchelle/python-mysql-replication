import datetime
import decimal
import struct
import sys


def is_data_short(data: bytes, expected: int):
    if len(data) < expected:
        return True
    return False


def decode_count(data: bytes, is_small: bool):
    if is_small:
        return parse_uint16(data)
    else:
        return parse_uint32(data)


def decode_uint(data: bytes):
    if is_data_short(data, 2):
        return 0
    return parse_uint16(data)


def length_encoded_int(data: bytes):
    if len(data) == 0:
        return 0, True, 0

    if data[0] == 251:
        return None, True, 1

    if data[0] == 252:
        return parse_uint16(data[1:]), False, 3

    if data[0] == 253:
        return parse_uint24(data[1:]), False, 4

    if data[0] == 254:
        return (
            parse_uint64(data[1:]),
            False,
            9,
        )

    return data[0], False, 1


def decode_variable_length(data: bytes):
    max_count = 5
    if len(data) < max_count:
        max_count = len(data)
    pos = 0
    length = 0
    for _ in range(max_count):
        v = data[pos]
        length |= (v & 0x7F) << (7 * pos)
        pos += 1
        if v & 0x80 == 0:
            if length > sys.maxsize - 1:
                return 0, 0
            return int(length), pos

    return 0, 0


def parse_decimal_from_bytes(
    raw_decimal: bytes, precision: int, decimals: int
) -> decimal.Decimal:
    """
    Parse decimal from bytes.
    """
    digits_per_integer = 9
    compressed_bytes = [0, 1, 1, 2, 2, 3, 3, 4, 4, 4]
    integral = precision - decimals

    uncomp_integral, comp_integral = divmod(integral, digits_per_integer)
    uncomp_fractional, comp_fractional = divmod(decimals, digits_per_integer)

    res = "-" if not raw_decimal[0] & 0x80 else ""
    mask = -1 if res == "-" else 0
    raw_decimal = bytearray([raw_decimal[0] ^ 0x80]) + raw_decimal[1:]

    def decode_decimal_decompress_value(comp_indx, data, mask):
        size = compressed_bytes[comp_indx]
        if size > 0:
            databuff = bytearray(data[:size])
            for i in range(size):
                databuff[i] = (databuff[i] ^ mask) & 0xFF
            return size, int.from_bytes(databuff, byteorder="big")
        return 0, 0

    pointer, value = decode_decimal_decompress_value(comp_integral, raw_decimal, mask)
    res += str(value)

    for _ in range(uncomp_integral):
        value = struct.unpack(">i", raw_decimal[pointer : pointer + 4])[0] ^ mask
        res += f"{value:09}"
        pointer += 4

    res += "."

    for _ in range(uncomp_fractional):
        value = struct.unpack(">i", raw_decimal[pointer : pointer + 4])[0] ^ mask
        res += f"{value:09}"
        pointer += 4

    size, value = decode_decimal_decompress_value(
        comp_fractional, raw_decimal[pointer:], mask
    )
    if size > 0:
        res += f"{value:0{comp_fractional}d}"
    return decimal.Decimal(res)


def decode_decimal(data: bytes):
    return parse_decimal_from_bytes(data[2:], data[0], data[1])


def decode_time(data: bytes):
    v = parse_int64(data)

    if v == 0:
        return datetime.time(hour=0, minute=0, second=0)

    if v < 0:
        v = -v
    int_part = v >> 24
    hour = (int_part >> 12) % (1 << 10)
    min = (int_part >> 6) % (1 << 6)
    sec = int_part % (1 << 6)
    frac = v % (1 << 24)
    return datetime.time(hour=hour, minute=min, second=sec, microsecond=frac)


def decode_datetime(data):
    v = parse_int64(data)

    if v == 0:
        # datetime parse Error
        return "0000-00-00 00:00:00"

    if v < 0:
        v = -v

    int_part = v >> 24
    ymd = int_part >> 17
    ym = ymd >> 5
    hms = int_part % (1 << 17)

    year = ym // 13
    month = ym % 13
    day = ymd % (1 << 5)
    hour = hms >> 12
    minute = (hms >> 6) % (1 << 6)
    second = hms % (1 << 6)
    frac = v % (1 << 24)

    return datetime.datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=frac,
    )


def parse_int16(data: bytes):
    return struct.unpack("<h", data[:2])[0]


def parse_uint16(data: bytes):
    return struct.unpack("<H", data[:2])[0]


def parse_uint24(data: bytes):
    try:
        return (
            struct.unpack("B", data[0])[0]
            + (struct.unpack("B", data[1])[0] << 8)
            + (struct.unpack("B", data[2])[0] << 16)
        )
    except TypeError:
        return data[0] + (data[1] << 8) + (data[2] << 16)


def parse_int32(data: bytes):
    return struct.unpack("<i", data[:4])[0]


def parse_uint32(data: bytes):
    return struct.unpack("<I", data[:4])[0]


def parse_int64(data: bytes):
    return struct.unpack("<q", data[:8])[0]


def parse_uint64(data: bytes):
    return struct.unpack("<Q", data[:8])[0]


def parse_double(data: bytes):
    return struct.unpack("<d", data[:8])[0]


def parse_string(n: int, length: int, data: bytes):
    data = data[n:]
    return data[:length]
