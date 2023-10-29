from pymysqlreplication.util.bytes import *
from pymysqlreplication.constants import FIELD_TYPE
from enum import Enum

JSONB_TYPE_SMALL_OBJECT = 0x0
JSONB_TYPE_LARGE_OBJECT = 0x1
JSONB_TYPE_SMALL_ARRAY = 0x2
JSONB_TYPE_LARGE_ARRAY = 0x3
JSONB_TYPE_LITERAL = 0x4
JSONB_TYPE_INT16 = 0x5
JSONB_TYPE_UINT16 = 0x6
JSONB_TYPE_INT32 = 0x7
JSONB_TYPE_UINT32 = 0x8
JSONB_TYPE_INT64 = 0x9
JSONB_TYPE_UINT64 = 0xA
JSONB_TYPE_DOUBLE = 0xB
JSONB_TYPE_STRING = 0xC
JSONB_TYPE_OPAQUE = 0xF

JSONB_LITERAL_NULL = 0x0
JSONB_LITERAL_TRUE = 0x1
JSONB_LITERAL_FALSE = 0x2

JSONB_SMALL_OFFSET_SIZE = 2
JSONB_LARGE_OFFSET_SIZE = 4
JSONB_KEY_ENTRY_SIZE_SMALL = 2 + JSONB_SMALL_OFFSET_SIZE
JSONB_KEY_ENTRY_SIZE_LARGE = 2 + JSONB_LARGE_OFFSET_SIZE
JSONB_VALUE_ENTRY_SIZE_SMALL = 1 + JSONB_SMALL_OFFSET_SIZE
JSONB_VALUE_ENTRY_SIZE_LARGE = 1 + JSONB_LARGE_OFFSET_SIZE


def is_json_inline_value(type: bytes, is_small: bool) -> bool:
    if type in [JSONB_TYPE_UINT16, JSONB_TYPE_INT16, JSONB_TYPE_LITERAL]:
        return True
    elif type in [JSONB_TYPE_INT32, JSONB_TYPE_UINT32]:
        return not is_small
    return False


def parse_json(type: bytes, data: bytes):
    if type == JSONB_TYPE_SMALL_OBJECT:
        v = parse_json_object_or_array(data, True, True)
    elif type == JSONB_TYPE_LARGE_OBJECT:
        v = parse_json_object_or_array(data, False, True)
    elif type == JSONB_TYPE_SMALL_ARRAY:
        v = parse_json_object_or_array(data, True, False)
    elif type == JSONB_TYPE_LARGE_ARRAY:
        v = parse_json_object_or_array(data, False, False)
    elif type == JSONB_TYPE_LITERAL:
        v = parse_literal(data)
    elif type == JSONB_TYPE_INT16:
        v = parse_int16(data)
    elif type == JSONB_TYPE_UINT16:
        v = parse_uint16(data)
    elif type == JSONB_TYPE_INT32:
        v = parse_int32(data)
    elif type == JSONB_TYPE_UINT32:
        v = parse_uint32(data)
    elif type == JSONB_TYPE_INT64:
        v = parse_int64(data)
    elif type == JSONB_TYPE_UINT64:
        v = parse_uint64(data)
    elif type == JSONB_TYPE_DOUBLE:
        v = parse_double(data)
    elif type == JSONB_TYPE_STRING:
        length, n = decode_variable_length(data)
        v = parse_string(n, length, data)
    elif type == JSONB_TYPE_OPAQUE:
        v = parse_opaque(data)
    else:
        raise ValueError(f"Json type {type} is not handled")
    return v


def parse_json_object_or_array(bytes, is_small, is_object):
    offset_size = JSONB_SMALL_OFFSET_SIZE if is_small else JSONB_LARGE_OFFSET_SIZE
    count = decode_count(bytes, is_small)
    size = decode_count(bytes[offset_size:], is_small)
    if is_small:
        key_entry_size = JSONB_KEY_ENTRY_SIZE_SMALL
        value_entry_size = JSONB_VALUE_ENTRY_SIZE_SMALL
    else:
        key_entry_size = JSONB_KEY_ENTRY_SIZE_LARGE
        value_entry_size = JSONB_VALUE_ENTRY_SIZE_LARGE
    if is_data_short(bytes, size):
        raise ValueError(
            "Before MySQL 5.7.22, json type generated column may have invalid value"
        )

    header_size = 2 * offset_size + count * value_entry_size

    if is_object:
        header_size += count * key_entry_size

    if header_size > size:
        raise ValueError("header size > size")

    keys = []
    if is_object:
        keys = []
        for i in range(count):
            entry_offset = 2 * offset_size + key_entry_size * i
            key_offset = decode_count(bytes[entry_offset:], is_small)
            key_length = decode_uint(bytes[entry_offset + offset_size :])
            keys.append(bytes[key_offset : key_offset + key_length])

    values = {}
    for i in range(count):
        entry_offset = 2 * offset_size + value_entry_size * i
        if is_object:
            entry_offset += key_entry_size * count
        json_type = bytes[entry_offset]
        if is_json_inline_value(json_type, is_small):
            values[i] = parse_json(
                json_type, bytes[entry_offset + 1 : entry_offset + value_entry_size]
            )
            continue
        value_offset = decode_count(bytes[entry_offset + 1 :], is_small)
        if is_data_short(bytes, value_offset):
            return None
        values[i] = parse_json(json_type, bytes[value_offset:])
    if not is_object:
        return list(values.values())
    out = {}
    for i in range(count):
        out[keys[i]] = values[i]
    return out


def parse_literal(data: bytes):
    json_type = data[0]
    if json_type == JSONB_LITERAL_NULL:
        return None
    elif json_type == JSONB_LITERAL_TRUE:
        return True
    elif json_type == JSONB_LITERAL_FALSE:
        return False

    raise ValueError("NOT LITERAL TYPE")


def parse_opaque(data: bytes):
    if is_data_short(data, 1):
        return None
    type_ = data[0]
    data = data[1:]

    length, n = decode_variable_length(data)
    data = data[n : n + length]

    if type_ in [FIELD_TYPE.NEWDECIMAL, FIELD_TYPE.DECIMAL]:
        return decode_decimal(data)
    elif type_ in [FIELD_TYPE.TIME, FIELD_TYPE.TIME2]:
        return decode_time(data)
    elif type_ in [FIELD_TYPE.DATE, FIELD_TYPE.DATETIME, FIELD_TYPE.DATETIME2]:
        return decode_datetime(data)
    else:
        return data.decode(errors="ignore")


class JsonDiffOperation(Enum):
    # The JSON value in the given path is replaced with a new value.
    # It has the same effect as `JSON_REPLACE(col, path, value)`.
    Replace = 0
    # Add a new element at the given path.
    # If the path specifies an array element, it has the same effect as `JSON_ARRAY_INSERT(col, path, value)`.
    # If the path specifies an object member, it has the same effect as `JSON_INSERT(col, path, value)`.
    Insert = 1
    # The JSON value at the given path is removed from an array or object.
    # It has the same effect as `JSON_REMOVE(col, path)`.
    Remove = 2

    @staticmethod
    def by_index(index):
        return JsonDiffOperation(index)


class JsonDiff:
    # JsonDiffOperation Remove Operation Does not have Value
    def __init__(self, op: JsonDiffOperation, path: bytes, value=None):
        self.op = op
        self.path = path
        self.value = value

    def __str__(self):
        return f"JsonDiff(op :{self.op} path :{self.path.decode()} value :{self.value.decode() if self.value else ''})"
