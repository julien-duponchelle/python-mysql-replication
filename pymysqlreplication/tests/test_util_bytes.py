from pymysqlreplication.util import *
from pymysqlreplication.tests.base import PyMySQLReplicationTestCase

"""
These tests aim to cover some potential input scenarios, including valid inputs, edge cases, and error handling.
This approach ensures that every line of the corresponding function is executed under test conditions, 
thereby improving the coverage.
"""


class TestIsDataShort(PyMySQLReplicationTestCase):
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


class TestDecodeCount(PyMySQLReplicationTestCase):
    def test_small_format(self):
        # Test with 2-byte input and small format.
        data = bytearray([0x01, 0x00])
        is_small = True
        result = decode_count(data, is_small)
        self.assertEqual(result, 1)

    def test_large_format(self):
        # Test with 4-byte input and large format.
        data = bytearray([0x01, 0x00, 0x00, 0x00])
        is_small = False
        result = decode_count(data, is_small)
        self.assertEqual(result, 1)


class TestDecodeUint(PyMySQLReplicationTestCase):
    def test_valid_input(self):
        # Test with a known 2-byte input.
        data = bytearray([0x01, 0x00])
        result = decode_uint(data)
        self.assertEqual(result, 1)

    def test_short_data(self):
        # Test with a 1-byte input, which is less than expected.
        data = bytearray([0x01])
        result = decode_uint(data)
        self.assertEqual(result, 0)

    def test_empty_data(self):
        data = bytearray([])
        result = decode_uint(data)
        self.assertEqual(result, 0)


class TestDecodeVariableLength(PyMySQLReplicationTestCase):
    def test_single_byte(self):
        # Test with a single byte where the high bit is not set (indicating the end)
        data = bytearray([0x05])  # 5 with the high bit not set
        length, pos = decode_variable_length(data)
        self.assertEqual(length, 5)
        self.assertEqual(pos, 1)

    def test_multiple_bytes(self):
        # Test with multiple bytes
        # 0x81 -> 1 with the high bit set, indicating more bytes
        # 0x01 -> 1 with the high bit not set, indicating the end
        # Combined value is 1 + (1 << 7) = 129
        data = bytearray([0x81, 0x01])
        length, pos = decode_variable_length(data)
        self.assertEqual(length, 129)
        self.assertEqual(pos, 2)

    def test_max_length(self):
        # Test with the maximum length (5 bytes)
        # This will test the boundary condition of the loop in the function
        data = bytearray(
            [0x80, 0x80, 0x80, 0x80, 0x01]
        )  # Each 0x80 has the high bit set, 0x01 does not
        # The value is 1 << (7 * 4) = 2**28
        length, pos = decode_variable_length(data)
        self.assertEqual(length, 2**28)
        self.assertEqual(pos, 5)


class TestParseUint16(PyMySQLReplicationTestCase):
    def test_valid_input(self):
        data = bytearray([0x01, 0x00])
        result = parse_uint16(data)
        self.assertEqual(result, 1)

    def test_different_input(self):
        data = bytearray([0xFF, 0x00])  # Represents the unsigned integer 255
        result = parse_uint16(data)
        self.assertEqual(result, 255)


class TestLengthEncodedInt(PyMySQLReplicationTestCase):
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


class TestDecodeTime(PyMySQLReplicationTestCase):
    def test_midnight(self):
        data = bytearray([0x00] * 8)  # Represents 00:00:00
        result = decode_time(data)
        self.assertEqual(result, datetime.time(0, 0, 0))

    def test_valid_time(self):
        data = bytearray(
            [0x00, 0x00, 0x00, 0xC0, 0x18, 0x01, 0x00, 0x00]
        )  # Represents 17:35:00
        result = decode_time(data)
        self.assertEqual(result, datetime.time(17, 35, 0))


class TestDecodeDatetime(PyMySQLReplicationTestCase):
    def test_zero_datetime(self):
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
