class TableMetadataUnavailableError(Exception):
    def __init__(self, table, cluster):
        Exception.__init__(self,"Unable to find metadata for table {t}".format(table))
