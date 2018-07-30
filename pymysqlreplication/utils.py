import re
from pkg_resources import parse_version


class Utils:
    def is_checksum_supported(self, server_version):

        version_number = \
            parse_version(re.findall('^([\d\.]+)', server_version)[0])
        if parse_version('5.6.1') <= version_number or \
                (("mariadb" in server_version.lower()) and
                 (parse_version('5.3') <= version_number)):
                return True

        return False
