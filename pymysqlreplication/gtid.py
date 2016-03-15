# -*- coding: utf-8 -*-

import re
import struct
import binascii


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
        m = re.search('^([0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12})((?::[0-9-]+)+)$', gtid)
        if not m:
            raise ValueError('GTID format is incorrect: %r' % (gtid, ))

        sid = m.group(1)
        intervals = m.group(2)

        intervals_parsed = [Gtid.parse_interval(x) for x in intervals.split(':')[1:]]

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
        return (16 + # sid
                8 + # n_intervals
                2 * # stop/start
                8 * # stop/start mark encoded as int64
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


class GtidSet(object):
    def __init__(self, gtid_set):
        if not gtid_set:
            self.gtids = []
        else:
            self.gtids = [Gtid(x.strip(' \n')) for x in gtid_set.split(',')]

    def __str__(self):
        return ','.join(str(x) for x in self.gtids)

    def __repr__(self):
        return '<GtidSet "%s"' % ','.join(repr(x) for x in self.gtids)

    @property
    def encoded_length(self):
        return (8 + # n_sids
                sum(x.encoded_length for x in self.gtids))

    def encoded(self):
        return b'' + (struct.pack('<Q', len(self.gtids)) +
                b''.join(x.encode() for x in self.gtids))
