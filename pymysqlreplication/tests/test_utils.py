import unittest

from pymysqlreplication import utils


class TestUtils(unittest.TestCase):
    @staticmethod
    def test_is_checksum_supported():
        # regular supported mysql version
        server_version = '5.7.17-log'
        assert utils.is_checksum_supported(server_version) is True

        # mariaDB supported mysql version
        server_version = '10.2.11-MariaDB-10.2.11+maria~jessie-log'
        assert utils.is_checksum_supported(server_version) is True

        # regular unsupported mysql version
        server_version = '5.3.1-log'
        assert utils.is_checksum_supported(server_version) is False

        # mariaDB unsupported mysql version
        server_version = '5.2.11-MariaDB'
        assert utils.is_checksum_supported(server_version) is False

        server_version = '5.2.11-mariadb'
        assert utils.is_checksum_supported(server_version) is False
