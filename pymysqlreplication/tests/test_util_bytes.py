import unittest
from pymysqlreplication.util import *


class TestIsDataShort(unittest.TestCase):
    def test_data_is_shorter(self):
        data = bytearray([0x01])
        expected_length = 2
        self.assertTrue(is_data_short(data, expected_length))

    def test_data_is_equal_length(self):
        data = bytearray([0x01, 0x00])
        expected_length = 2
        self.assertFalse(is_data_short(data, expected_length))

    def test_data_is_longer(self):
        data = bytearray([0x01, 0x00, 0x02])
        expected_length = 2
        self.assertFalse(is_data_short(data, expected_length))

    def test_data_is_empty(self):
        data = bytearray([])
        expected_length = 1
        self.assertTrue(is_data_short(data, expected_length))


class TestDecodeCount(unittest.TestCase):
    def test_small_format(self):
        data = bytearray([0x01, 0x00])
        is_small = True
        result = decode_count(data, is_small)
        self.assertEqual(result, 1)

    def test_large_format(self):
        data = bytearray([0x01, 0x00, 0x00, 0x00])
        is_small = False
        result = decode_count(data, is_small)
        self.assertEqual(result, 1)


class TestDecodeUint(unittest.TestCase):
    def test_valid_input(self):
        data = bytearray([0x01, 0x00])
        result = decode_uint(data)
        self.assertEqual(result, 1)

    def test_short_data(self):
        data = bytearray([0x01])
        result = decode_uint(data)
        self.assertEqual(result, 0)

    def test_empty_data(self):
        data = bytearray([])
        result = decode_uint(data)
        self.assertEqual(result, 0)


class TestDecodeVariableLength(unittest.TestCase):
    def test_single_byte(self):
        data = bytearray([0x05])
        length, pos = decode_variable_length(data)
        self.assertEqual(length, 5)
        self.assertEqual(pos, 1)

    def test_multiple_bytes(self):
        data = bytearray([0x81, 0x01])
        length, pos = decode_variable_length(data)
        self.assertEqual(length, 129)
        self.assertEqual(pos, 2)

    def test_max_length(self):
        data = bytearray([0x80, 0x80, 0x80, 0x80, 0x01])
        length, pos = decode_variable_length(data)
        self.assertEqual(length, 2**28)
        self.assertEqual(pos, 5)


class TestParseUint16(unittest.TestCase):
    def test_valid_input(self):
        data = bytearray([0x01, 0x00])
        result = parse_uint16(data)
        self.assertEqual(result, 1)

    def test_different_input(self):
        data = bytearray([0xFF, 0x00])
        result = parse_uint16(data)
        self.assertEqual(result, 255)


class TestLengthEncodedInt(unittest.TestCase):
    def test_single_byte(self):
        data = bytearray([0x05])
        result, _, _ = length_encoded_int(data)
        self.assertEqual(result, 5)

    def test_two_bytes(self):
        data = bytearray([0xFC, 0x12, 0x34])
        result, _, _ = length_encoded_int(data)
        self.assertEqual(result, 0x3412)

    def test_three_bytes(self):
        data = bytearray([0xFD, 0x01, 0x02, 0x03])
        result, _, _ = length_encoded_int(data)
        self.assertEqual(result, 0x030201)


class TestDecodeTime(unittest.TestCase):
    def test_midnight(self):
        data = bytearray([0x00] * 8)
        result = decode_time(data)
        self.assertEqual(result, datetime.time(0, 0, 0))

    def test_valid_time(self):
        data = bytearray([0x00, 0x00, 0x00, 0xC0, 0x18, 0x01, 0x00, 0x00])
        result = decode_time(data)
        self.assertEqual(result, datetime.time(17, 35, 0))


class TestDecodeDatetime(unittest.TestCase):
    def test_zero_datetime(self):
        data = bytearray([0x00] * 8)
        result = decode_datetime(data)
        self.assertEqual(result, "0000-00-00 00:00:00")

    def test_valid_datetime(self):
        data = bytearray([0x00, 0x00, 0x00, 0xC0, 0x18, 0x9B, 0xB1, 0x19])
        expected_datetime = datetime.datetime(
            year=2023, month=11, day=13, hour=17, minute=35, second=0
        )
        result = decode_datetime(data)
        self.assertEqual(result, expected_datetime)


if __name__ == "__main__":
    unittest.main()
