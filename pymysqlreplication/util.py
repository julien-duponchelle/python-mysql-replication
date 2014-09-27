import struct

def byte2int(b):
    return struct.unpack("!B", b)[0]

def int2byte(i):
    return struct.pack("!B", i)
