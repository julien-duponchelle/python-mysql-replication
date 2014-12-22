# -*- coding: utf-8 -*-

import struct

class Bitmap(object):
    """ Use for current-present-bitmap1/2 in RowsEvent, copy from MySQL mysys/my_bitmap.c
    See http://dev.mysql.com/doc/internals/en/rows-event.html
        
        null bitmap length = (bits set in 'columns-present-bitmap1'+7)/8
        null bitmap2 length = (bits set in 'columns-present-bitmap2'+7)/8

    We can not calculate the length using column count directly in minimal or noblob binlog row image.  

    """ 

    bits2Nbits = [
        0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
        4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8,
    ]

    def __init__(self, bitmap, nbits):
        self._nbits = int(nbits)   
        self._bitmap = bytearray(b'\x00' * int((self._nbits + 31) / 32) * 4)
        self._bitmap[0:len(bitmap)] = bitmap
        self._lastWordMask = 0
        self._createLastWordMask()

    def _countBitsUint32(self, v):
        s = bytearray(struct.pack("<I", v))
        return self.bits2Nbits[s[0]] + self.bits2Nbits[s[1]] + self.bits2Nbits[s[2]] + self.bits2Nbits[s[3]]

    def _createLastWordMask(self):
        used = 1 + (self._nbits - 1) & 0x7
        mask = (~(1 << used) - 1) & 0xFF

        b = bytearray(0)
        l = int((self._nbits + 7) / 8) & 0x3
        if l == 1:
            self._lastWordMask = ~0 & 0xFFFFFFFF
            b = bytearray(struct.pack("<I", self._lastWordMask))
            b[0] = mask
        elif l == 2:
            self._lastWordMask = ~0 & 0xFFFFFFFF
            b = bytearray(struct.pack("<I", self._lastWordMask))
            b[0] = 0
            b[1] = mask
        elif l == 3:
            self._lastWordMask = 0
            b = bytearray(struct.pack("<I", self._lastWordMask))
            b[2] = mask
            b[3] = 0xFF
        elif l == 0:
            self._lastWordMask = 0
            b = bytearray(struct.pack("<I", self._lastWordMask))
            b[3] = mask

        self._lastWordMask = struct.unpack("<I", bytes(b))[0]

    def bits_set(self):
        res = 0
        for i in range(0, int(len(self._bitmap) / 4) - 1):
            res += self._countBitsUint32(struct.unpack("<I", bytes(self._bitmap[i*4:i*4 + 4]))[0])

        res += self._countBitsUint32(struct.unpack("<I", bytes(self._bitmap[-4:]))[0] & ~self._lastWordMask)

        return res

    def is_set(self, bit):
        return self._bitmap[int(bit / 8)] & (1 << (bit & 7))
