import unittest
from pymysqlreplication.util import *


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
    def test_valid_time(self):
        # Assuming parse_int64 returns an integer representing time
        # Here we use a mocked function for parse_int64
        data = bytearray(8)  # Mocked data, replace with actual test data
        with unittest.mock.patch(
            "pymysqlreplication.util.parse_int64", return_value=12345678
        ):
            result = decode_time(data)
            self.assertIsInstance(result, datetime.time)


# Running the tests
if __name__ == "__main__":
    unittest.main()
