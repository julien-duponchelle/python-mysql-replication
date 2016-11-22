class TableMetadataUnavailableError(Exception):
    def __init__(self, table):
        Exception.__init__(self,"Unable to find metadata for table {0}".format(table))
