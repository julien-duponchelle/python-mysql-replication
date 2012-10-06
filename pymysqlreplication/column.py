import struct
from pymysql.constants import FIELD_TYPE
from pymysql.util import byte2int, int2byte 

class Column(object):
    '''Definition of a column'''

    def __init__(self, column_type, packet):
        self.type = column_type
        if self.type == FIELD_TYPE.STRING:
            self.__read_string_metadata()
        elif self.type == FIELD_TYPE.VAR_STRING:
            self.__read_string_metadata()
        elif self.type == FIELD_TYPE.VARCHAR:
            self.max_length = struct.unpack('<H', packet.read(2))[0]
        elif self.type == FIELD_TYPE.BLOB:
            pass #1
        elif self.type == FIELD_TYPE.DECIMAL:
            pass #2
        elif self.type == FIELD_TYPE.NEWDECIMAL:
            self.precision = struct.unpack('<B', packet.read(1))[0]
            self.decimals = struct.unpack('<B', packet.read(1))[0]
        elif self.type == FIELD_TYPE.DOUBLE:
            pass #1
        elif self.type == FIELD_TYPE.FLOAT:
            pass #1
        elif self.type == FIELD_TYPE.ENUM:
            pass #2
        elif self.type == FIELD_TYPE.SET:
            pass #2

    def __read_string_metadata(self):
        pass


