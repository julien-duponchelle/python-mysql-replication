import unittest
from datetime import time

from pymysqlreplication.util import *


class TestIsDataShort(unittest.TestCase):
    def test_data_is_shorter(self):
        # Test with data shorter than expected.
        data = bytearray([0x01])  # 1-byte data
        expected_length = 2
        self.assertTrue(is_data_short(data, expected_length))

    def test_data_is_equal_length(self):
        # Test with data equal to expected length.
        data = bytearray([0x01, 0x00])  # 2-byte data
        expected_length = 2
        self.assertFalse(is_data_short(data, expected_length))

    def test_data_is_longer(self):
        # Test with data longer than expected.
        data = bytearray([0x01, 0x00, 0x02])  # 3-byte data
        expected_length = 2
        self.assertFalse(is_data_short(data, expected_length))

    def test_data_is_empty(self):
        # Test with empty data.
        data = bytearray([])
        expected_length = 1
        self.assertTrue(is_data_short(data, expected_length))


class TestDecodeCount(unittest.TestCase):
    def test_small_format(self):
        # Test with 2-byte input and small format.
        data = bytearray([0x01, 0x00])  # Represents the unsigned integer 1
        is_small = True
        result = decode_count(data, is_small)
        self.assertEqual(result, 1)

    def test_large_format(self):
        # Test with 4-byte input and large format.
        data = bytearray([0x01, 0x00, 0x00, 0x00])  # Represents the unsigned integer 1
        is_small = False
        result = decode_count(data, is_small)
        self.assertEqual(result, 1)


class TestDecodeUint(unittest.TestCase):
    def test_valid_input(self):
        # Test with a known 2-byte input.
        data = bytearray([0x01, 0x00])  # Represents the unsigned integer 1
        result = decode_uint(data)
        self.assertEqual(result, 1)

    def test_short_data(self):
        # Test with a 1-byte input, which is less than expected.
        data = bytearray([0x01])
        result = decode_uint(data)
        self.assertEqual(result, 0)

    def test_empty_data(self):
        # Test with an empty input.
        data = bytearray([])
        result = decode_uint(data)
        self.assertEqual(result, 0)


class TestParseUint16(unittest.TestCase):
    def test_valid_input(self):
        data = bytearray([0x01, 0x00])  # Represents the unsigned integer 1
        result = parse_uint16(data)
        self.assertEqual(result, 1)

    def test_different_input(self):
        data = bytearray([0xFF, 0x00])  # Represents the unsigned integer 255
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
        # Test decoding of midnight
        data = bytearray([0x00] * 8)  # Represents 00:00:00
        result = decode_time(data)
        self.assertEqual(result, datetime.time(0, 0, 0))

    def test_valid_time(self):
        data = bytearray(
            [0x00, 0x00, 0x00, 0xC0, 0x18, 0x01, 0x00, 0x00]
        )  # Represents 17:35:00
        result = decode_time(data)
        self.assertEqual(result, datetime.time(17, 35, 0))


class TestDecodeDatetime(unittest.TestCase):
    def test_zero_datetime(self):
        # Test decoding of zero datetime
        data = bytearray([0x00] * 8)  # Represents 0000-00-00 00:00:00
        result = decode_datetime(data)
        self.assertEqual(result, "0000-00-00 00:00:00")

    def test_valid_datetime(self):
        data = bytearray(
            [0x00, 0x00, 0x00, 0xC0, 0x18, 0x9B, 0xB1, 0x19]
        )  # Represents 2023-11-13 17:35:00
        expected_datetime = datetime.datetime(
            year=2023, month=11, day=13, hour=17, minute=35, second=0
        )
        result = decode_datetime(data)
        self.assertEqual(result, expected_datetime)


# Running the tests
if __name__ == "__main__":
    unittest.main()
