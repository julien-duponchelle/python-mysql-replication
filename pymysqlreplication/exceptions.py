class TableMetadataUnavailableError(Exception):
    def __init__(self, table):
        Exception.__init__(self, f"Unable to find metadata for table {table}")


class BinLogNotEnabled(Exception):
    def __init__(self):
        Exception.__init__(self, "MySQL binary logging is not enabled.")


class StatusVariableMismatch(Exception):
    def __init__(self):
        Exception.__init__(
            self,
            " ".join(
                (
                    "Unknown status variable in query event.",
                    "Possible parse failure in preceding fields",
                    "or outdated constants.STATUS_VAR_KEY",
                    "Refer to MySQL documentation/source code",
                    "or create an issue on GitHub",
                )
            ),
        )
