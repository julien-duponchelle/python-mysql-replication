import re
import struct
import binascii
from copy import deepcopy
from io import BytesIO


def overlap(i1, i2):
    return i1[0] < i2[1] and i1[1] > i2[0]


def contains(i1, i2):
    return i2[0] >= i1[0] and i2[1] <= i1[1]


class Gtid(object):
    """A mysql GTID is composed of a server-id and a set of right-open
    intervals [a,b), and represent all transactions x that happened on
    server SID such as

        a <= x < b

    The human representation of it, though, is either represented by a
    single transaction number A=a (when only one transaction is covered,
    ie b = a+1)

        SID:A

    Or a closed interval [A,B] for at least two transactions (note, in that
    case, that b=B+1)

        SID:A-B

    We can also have a mix of ranges for a given SID:
        SID:1-2:4:6-74

    For convenience, a Gtid accepts adding Gtid's to it and will merge
    the existing interval representation. Adding TXN 3 to the human
    representation above would produce:

        SID:1-4:6-74

    and adding 5 to this new result:

        SID:1-74

    Raises:
        ValueError: If construction parsing from string fails
        Exception: Adding an already present transaction number (one that overlaps).
        Exception: Adding a Gtid with a different SID.
    """

    @staticmethod
    def parse_interval(interval):
        """
        We parse a human-generated string here. So our end value b
        is incremented to conform to the internal representation format.

        Raises:
            - ValueError if GTID format is incorrect
        """
        m = re.search("^([0-9]+)(?:-([0-9]+))?$", interval)
        if not m:
            raise ValueError(f"GTID format is incorrect: {interval!r}")
        a = int(m.group(1))
        b = int(m.group(2) or a)
        return a, b + 1

    @staticmethod
    def parse(gtid):
        """Parse a GTID from mysql textual format.

        Raises:
            - ValueError: if GTID format is incorrect.
        """
        m = re.search(
            "^([0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12})"
            "((?::[0-9-]+)+)$",
            gtid,
        )
        if not m:
            raise ValueError(f"GTID format is incorrect: {gtid!r}")

        sid = m.group(1)
        intervals = m.group(2)

        intervals_parsed = [Gtid.parse_interval(x) for x in intervals.split(":")[1:]]

        return sid, intervals_parsed

    def __add_interval(self, itvl):
        """
        Use the internal representation format and add it
        to our intervals, merging if required.

        Raises:
            Exception: if Malformated interval or Overlapping interval
        """
        new = []

        if itvl[0] > itvl[1]:
            raise Exception(f"Malformed interval {itvl}")

        if any(overlap(x, itvl) for x in self.intervals):
            raise Exception(f"Overlapping interval {itvl}")

        ## Merge: arrange interval to fit existing set
        for existing in sorted(self.intervals):
            if itvl[0] == existing[1]:
                itvl = (existing[0], itvl[1])
                continue

            if itvl[1] == existing[0]:
                itvl = (itvl[0], existing[1])
                continue

            new.append(existing)

        self.intervals = sorted(new + [itvl])

    def __sub_interval(self, itvl):
        """Using the internal representation, remove an interval

        Raises: Exception if itvl malformated"""
        new = []

        if itvl[0] > itvl[1]:
            raise Exception(f"Malformed interval {itvl}")

        if not any(overlap(x, itvl) for x in self.intervals):
            # No raise
            return

        ## Merge: arrange existing set around interval
        for existing in sorted(self.intervals):
            if overlap(existing, itvl):
                if existing[0] < itvl[0]:
                    new.append((existing[0], itvl[0]))
                if existing[1] > itvl[1]:
                    new.append((itvl[1], existing[1]))
            else:
                new.append(existing)

        self.intervals = new

    def __contains__(self, other):
        """Test if other is contained within self.
        First we compare sid they must be equals.

        Then we search if intervals from other are contained within
        self intervals.
        """
        if other.sid != self.sid:
            return False

        return all(
            any(contains(me, them) for me in self.intervals) for them in other.intervals
        )

    def __init__(self, gtid, sid=None, intervals=[]):
        if sid:
            intervals = intervals
        else:
            sid, intervals = Gtid.parse(gtid)

        self.sid = sid
        self.intervals = []
        for itvl in intervals:
            self.__add_interval(itvl)

    def __add__(self, other):
        """Include the transactions of this gtid.

        Raises:
           Exception: if the attempted merge has different SID"""
        if self.sid != other.sid:
            raise Exception(f"Attempt to merge different SID {self.sid} != {other.sid}")

        result = deepcopy(self)

        for itvl in other.intervals:
            result.__add_interval(itvl)

        return result

    def __sub__(self, other):
        """Remove intervals. Do not raise, if different SID simply
        ignore"""
        result = deepcopy(self)
        if self.sid != other.sid:
            return result

        for itvl in other.intervals:
            result.__sub_interval(itvl)

        return result

    def __str__(self):
        """We represent the human value here - a single number
        for one transaction, or a closed interval (decrementing b)"""

        def format_interval(x):
            if x[0] + 1 != x[1]:
                return f"{x[0]}-{x[1] - 1}"
            return str(x[0])

        interval_string = ":".join(map(format_interval, self.intervals))
        return f"{self.sid}:{interval_string}"

    def __repr__(self):
        return f'<Gtid "{self}">'

    @property
    def encoded_length(self):
        return (
            16
            + 8  # sid
            + 2  # n_intervals
            * 8  # stop/start
            * len(self.intervals)  # stop/start mark encoded as int64
        )

    def encode(self):
        """Encode a Gtid in binary
        Bytes are in **little endian**.

        Format:

        - sid will be uncoded as hex-binary without the dashes as a [u8; 16]
        - size of the interval list as a u64
        - all the interval as a pair: (start: u64, end: u64).

        ## Diagram

        ```txt
        Alligned on u64 bit.
        +-+-+-+-+-+-+-+-+-+-+
        | sid [16;u8]       |
        |                   |
        +-+-+-+-+-+-+-+-+-+-+
        | intervals_len u64 |
        +-+-+-+-+-+-+-+-+-+-+
        |start u64             <-+
        - - - - - - - - - - -    + Repeated
        |stop u64              <-+  interval_len times
        - - - - - - - - - - -
        ```
        """
        buffer = b""
        # sid
        buffer += binascii.unhexlify(self.sid.replace("-", ""))
        # n_intervals
        buffer += struct.pack("<Q", len(self.intervals))

        for interval in self.intervals:
            # Start position
            buffer += struct.pack("<Q", interval[0])
            # Stop position
            buffer += struct.pack("<Q", interval[1])

        return buffer

    @classmethod
    def decode(cls, payload):
        """Decode from binary a Gtid

        :param BytesIO payload to decode
        """
        assert isinstance(payload, BytesIO), "payload is expected to be a BytesIO"
        sid = b""
        sid = sid + binascii.hexlify(payload.read(4))
        sid = sid + b"-"
        sid = sid + binascii.hexlify(payload.read(2))
        sid = sid + b"-"
        sid = sid + binascii.hexlify(payload.read(2))
        sid = sid + b"-"
        sid = sid + binascii.hexlify(payload.read(2))
        sid = sid + b"-"
        sid = sid + binascii.hexlify(payload.read(6))

        (n_intervals,) = struct.unpack("<Q", payload.read(8))
        intervals = []
        for i in range(0, n_intervals):
            start, end = struct.unpack("<QQ", payload.read(16))
            intervals.append((start, end - 1))

        def format_interval(x):
            if isinstance(x, tuple):
                return f"{x[0]}-{x[1]}"
            return f"{x}"

        intervals_string = ":".join([format_interval(x) for x in intervals])

        return cls(f"{sid.decode('ascii')}:{intervals_string}")

    def __eq__(self, other):
        if other.sid != self.sid:
            return False
        return self.intervals == other.intervals

    def __lt__(self, other):
        if other.sid != self.sid:
            return self.sid < other.sid
        return self.intervals < other.intervals

    def __le__(self, other):
        if other.sid != self.sid:
            return self.sid <= other.sid
        return self.intervals <= other.intervals

    def __gt__(self, other):
        if other.sid != self.sid:
            return self.sid > other.sid
        return self.intervals > other.intervals

    def __ge__(self, other):
        if other.sid != self.sid:
            return self.sid >= other.sid
        return self.intervals >= other.intervals


class GtidSet(object):
    """Represents a set of Gtid"""

    def __init__(self, gtid_set):
        """
        Construct a GtidSet initial state depends of the nature of `gtid_set` param.

        params:
          - gtid_set:
            - None: then the GtidSet start empty
            - a set of Gtid either as a their textual representation separated by comma
            - A set or list of gtid
            - A GTID alone.

        Raises:
          - ValueError: if `gtid_set` is a string separated with comma, but with malformated Gtid.
          - Exception: if Gtid interval are either malformated or overlapping
        """

        def _to_gtid(element):
            if isinstance(element, Gtid):
                return element
            return Gtid(element.strip(" \n"))

        if not gtid_set:
            self.gtids = []
        elif isinstance(gtid_set, (list, set)):
            self.gtids = [_to_gtid(x) for x in gtid_set]
        else:
            self.gtids = [Gtid(x.strip(" \n")) for x in gtid_set.split(",")]

    def merge_gtid(self, gtid):
        """Insert a Gtid in current GtidSet."""
        new_gtids = []
        for existing in self.gtids:
            if existing.sid == gtid.sid:
                new_gtids.append(existing + gtid)
            else:
                new_gtids.append(existing)
        if gtid.sid not in (x.sid for x in new_gtids):
            new_gtids.append(gtid)
        self.gtids = new_gtids

    def __contains__(self, other):
        """
        Test if self contains other, could be a GtidSet or a Gtid.

        Raises:
           - NotImplementedError other is not a GtidSet neither a Gtid,
            please convert it first to one of them
        """
        if isinstance(other, GtidSet):
            return all(other_gtid in self.gtids for other_gtid in other.gtids)
        if isinstance(other, Gtid):
            return any(other in x for x in self.gtids)
        raise NotImplementedError

    def __add__(self, other):
        """
        Merge current instance with an other GtidSet or with a Gtid alone.

        Raises:
            - NotImplementedError other is not a GtidSet neither a Gtid,
            please convert it first to one of them
        """
        if isinstance(other, Gtid):
            new = GtidSet(self.gtids)
            new.merge_gtid(other)
            return new

        if isinstance(other, GtidSet):
            new = GtidSet(self.gtids)
            for gtid in other.gtids:
                new.merge_gtid(gtid)
            return new

        raise NotImplementedError

    def __str__(self):
        """
        Returns a comma separated string of gtids.
        """
        return ",".join(str(x) for x in self.gtids)

    def __repr__(self):
        return f"<GtidSet {self.gtids}>"

    @property
    def encoded_length(self):
        return 8 + sum(x.encoded_length for x in self.gtids)  # n_sids

    def encoded(self):
        """Encode a GtidSet in binary
        Bytes are in **little endian**.

        - `n_sid`: u64 is the number of Gtid to read
        - `Gtid`: `n_sid` * `Gtid_encoded_size` times.
          See`Gtid.encode` documentation for details.

        ```txt
        Alligned on u64 bit.
        +-+-+-+-+-+-+-+-+-+-+
        | n_gtid u64        |
        +-+-+-+-+-+-+-+-+-+-+
        | Gtid              | - Repeated n_gtid times
        - - - - - - - - - - -
        ```
        """
        return b"" + (
            struct.pack("<Q", len(self.gtids))
            + b"".join(x.encode() for x in self.gtids)
        )

    encode = encoded

    @classmethod
    def decode(cls, payload):
        """Decode a GtidSet from binary.

        :param BytesIO payload to decode
        """
        assert isinstance(payload, BytesIO), "payload is expected to be a BytesIO"
        (n_sid,) = struct.unpack("<Q", payload.read(8))

        return cls([Gtid.decode(payload) for _ in range(0, n_sid)])

    def __eq__(self, other):
        return self.gtids == other.gtids
