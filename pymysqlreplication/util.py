import struct

def byte2int(b):
    try:
        return struct.unpack("!B", b)[0]
    except TypeError: #With python 3 some read return int
        return b

def int2byte(i):
    return struct.pack("!B", i)
