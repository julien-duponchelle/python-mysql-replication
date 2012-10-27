import struct
from pymysql.constants import FIELD_TYPE
from pymysql.util import byte2int, int2byte 

class Column(object):
    '''Definition of a column'''

    def __init__(self, column_type, column_schema, packet):
        self.type = column_type
        self.name = column_schema["COLUMN_NAME"]
        self.unsigned = False

        if column_schema["COLUMN_TYPE"].find("unsigned") != -1:
            self.unsigned = True
        if self.type == FIELD_TYPE.VAR_STRING or self.type == FIELD_TYPE.STRING:
            self.__read_string_metadata(packet, column_schema)
        elif self.type == FIELD_TYPE.VARCHAR:
            self.max_length = struct.unpack('<H', packet.read(2))[0]
        elif self.type == FIELD_TYPE.BLOB:
            self.length_size = packet.read_uint8()
        elif self.type == FIELD_TYPE.DECIMAL:
            pass #2
        elif self.type == FIELD_TYPE.NEWDECIMAL:
            self.precision = packet.read_uint8()
            self.decimals = packet.read_uint8()
        elif self.type == FIELD_TYPE.DOUBLE:
            pass #1
        elif self.type == FIELD_TYPE.FLOAT:
            pass #1

    def __read_string_metadata(self, packet, column_schema):
        metadata  = (packet.read_uint8() << 8) + packet.read_uint8()
        real_type = metadata >> 8
        if real_type == FIELD_TYPE.SET or real_type == FIELD_TYPE.ENUM:
            self.type = real_type
            self.size = metadata & 0x00ff
            self.__read_enum_metadata(column_schema)
        else:
            self.max_length = (((metadata >> 4) & 0x300) ^ 0x300) + (metadata & 0x00ff)

    def __read_enum_metadata(self, column_schema):
        enums = column_schema["COLUMN_TYPE"]
        if self.type == FIELD_TYPE.ENUM:
            self.enum_values = enums.replace('enum(', '').replace(')', '').replace('\'', '').split(',')
        else:
            self.set_values = enums.replace('set(', '').replace(')', '').replace('\'', '').split(',')
