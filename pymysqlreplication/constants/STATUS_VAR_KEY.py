#from enum import IntEnum

#class StatusVarsKey(IntEnum):
"""List of Query_event_status_vars
    
    A status variable in query events is a sequence of status KEY-VALUE pairs.
    The class variables enumerated below are KEYs.
    Each KEY determines the length of corresponding VALUE.

    For further details refer to:
    mysql-server: https://github.com/mysql/mysql-server/blob/beb865a960b9a8a16cf999c323e46c5b0c67f21f/libbinlogevents/include/statement_events.h#L463-L532
    MySQL Documentation: https://dev.mysql.com/doc/internals/en/query-event.html

    Status variable key names From mysql-server source code, edited by dongwook-chan
"""

# KEY
Q_FLAGS2_CODE = 0x00
Q_SQL_MODE_CODE = 0X01
Q_CATALOG_CODE = 0x02
Q_AUTO_INCREMENT = 0x03
Q_CHARSET_CODE = 0x04
Q_TIME_ZONE_CODE = 0x05
Q_CATALOG_NZ_CODE = 0x06
Q_LC_TIME_NAMES_CODE = 0x07
Q_CHARSET_DATABASE_CODE = 0x08
Q_TABLE_MAP_FOR_UPDATE_CODE = 0x09
Q_MASTER_DATA_WRITTEN_CODE = 0x0A
Q_INVOKER = 0x0B
Q_UPDATED_DB_NAMES = 0x0C   # MySQL only
Q_MICROSECONDS = 0x0D       # MySQL only
Q_COMMIT_TS = 0x0E
Q_COMMIT_TS2 = 0X0F
Q_EXPLICIT_DEFAULTS_FOR_TIMESTAMP = 0X10
Q_DDL_LOGGED_WITH_XID = 0X11
Q_DEFAULT_COLLATION_FOR_UTF8MB4 = 0X12
Q_SQL_REQUIRE_PRIMARY_KEY = 0X13
Q_DEFAULT_TABLE_ENCRYPTION = 0X14
Q_HRNOW = 0x80  # MariaDB only
Q_XID = 0x81    # MariaDB only