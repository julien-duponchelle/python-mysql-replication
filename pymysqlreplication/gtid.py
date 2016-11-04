# -*- coding: utf-8 -*-

import re
import struct
import binascii
from io import BytesIO


class Gtid(object):
    @staticmethod
    def parse_interval(interval):
        m = re.search('^([0-9]+)(?:-([0-9]+))?$', interval)
        if not m:
            raise ValueError('GTID format is incorrect: %r' % (interval, ))
        if not m.group(2):
            return (int(m.group(1)))
        else:
            return (int(m.group(1)), int(m.group(2)))

    @staticmethod
    def parse(gtid):
        m = re.search('^([0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12})'
                      '((?::[0-9-]+)+)$', gtid)
        if not m:
            raise ValueError('GTID format is incorrect: %r' % (gtid, ))

        sid = m.group(1)
        intervals = m.group(2)

        intervals_parsed = [Gtid.parse_interval(x)
                            for x in intervals.split(':')[1:]]

        return (sid, intervals_parsed)

    def __init__(self, gtid):
        self.sid = None
        self.intervals = []

        self.sid, self.intervals = Gtid.parse(gtid)

    def __str__(self):
        return '%s:%s' % (self.sid,
                          ':'.join(('%d-%s' % x) if isinstance(x, tuple)
                                   else str(x)
                                   for x in self.intervals))

    def __repr__(self):
        return '<Gtid "%s">' % self

    @property
    def encoded_length(self):
        return (16 +  # sid
                8 +  # n_intervals
                2 *  # stop/start
                8 *  # stop/start mark encoded as int64
                len(self.intervals))

    def encode(self):
        buffer = b''
        # sid
        buffer += binascii.unhexlify(self.sid.replace('-', ''))
        # n_intervals
        buffer += struct.pack('<Q', len(self.intervals))

        for interval in self.intervals:
            if isinstance(interval, tuple):
                # Do we have both a start and a stop position
                # Start position
                buffer += struct.pack('<Q', interval[0])
                # Stop position
                buffer += struct.pack('<Q', interval[1])
            else:
                # If we only have a start position
                # Like c63b8356-d74e-4870-8150-70eca127beb1:1,
                # the stop position is start + 1

                # Start position
                buffer += struct.pack('<Q', interval)
                # Stop position
                buffer += struct.pack('<Q', interval + 1)

        return buffer

    @classmethod
    def decode(cls, payload):
        assert isinstance(payload, BytesIO), \
            'payload is expected to be a BytesIO'
        sid = b''
        sid = sid + binascii.hexlify(payload.read(4))
        sid = sid + b'-'
        sid = sid + binascii.hexlify(payload.read(2))
        sid = sid + b'-'
        sid = sid + binascii.hexlify(payload.read(2))
        sid = sid + b'-'
        sid = sid + binascii.hexlify(payload.read(2))
        sid = sid + b'-'
        sid = sid + binascii.hexlify(payload.read(6))

        (n_intervals,) = struct.unpack('<Q', payload.read(8))
        intervals = []
        for i in range(0, n_intervals):
            start, end = struct.unpack('<QQ', payload.read(16))
            if end == start + 1:
                intervals.append(start)
            else:
                intervals.append((start, end))

        return cls('%s:%s' % (sid.decode('ascii'), ':'.join([
            '%d-%d' % x
            if isinstance(x, tuple)
            else '%d' % x
            for x in intervals])))


class GtidSet(object):
    def __init__(self, gtid_set):
        def _to_gtid(element):
            if isinstance(element, Gtid):
                return element
            return Gtid(element.strip(' \n'))

        if not gtid_set:
            self.gtids = []
        elif isinstance(gtid_set, (list, set)):
            self.gtids = [_to_gtid(x) for x in gtid_set]
        else:
            self.gtids = [Gtid(x.strip(' \n')) for x in gtid_set.split(',')]

    def __str__(self):
        return ','.join(str(x) for x in self.gtids)

    def __repr__(self):
        return '<GtidSet %r>' % self.gtids

    @property
    def encoded_length(self):
        return (8 +  # n_sids
                sum(x.encoded_length for x in self.gtids))

    def encoded(self):
        return b'' + (struct.pack('<Q', len(self.gtids)) +
                      b''.join(x.encode() for x in self.gtids))

    encode = encoded

    @classmethod
    def decode(cls, payload):
        assert isinstance(payload, BytesIO), \
            'payload is expected to be a BytesIO'
        (n_sid,) = struct.unpack('<Q', payload.read(8))

        return cls([Gtid.decode(payload) for _ in range(0, n_sid)])
