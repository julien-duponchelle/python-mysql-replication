.. _mysql57_support:

MySQL 5.7, MySQL 8.0+ and `use_column_name_cache`
==================================================

In MySQL 5.7 and earlier, the binary log events for row-based replication do not include column name metadata. This means that `python-mysql-replication` cannot map column values to their names directly from the binlog event.

Starting with MySQL 8.0.1, the `binlog_row_metadata` system variable was introduced to control the amount of metadata written to the binary log. This is a **GLOBAL** and **DYNAMIC** variable. The default value for this variable is `MINIMAL`, which provides the same behavior as MySQL 5.7.

The Problem
-----------

When column metadata is not present in the binlog (as in MySQL 5.7 and earlier, or when `binlog_row_metadata` is set to `MINIMAL` globally in MySQL 8.0+), the `values` dictionary in a `WriteRowsEvent`, `UpdateRowsEvent`, or `DeleteRowsEvent` will contain integer keys corresponding to the column index, not the column names.

For example, for a table `users` with columns `id` and `name`, an insert event might look like this:

.. code-block:: python

    {0: 1, 1: 'John Doe'}

This can make your replication logic harder to write and maintain, as you need to know the column order.

The Solution: `use_column_name_cache`
-------------------------------------

To address this, `python-mysql-replication` provides the `use_column_name_cache` parameter for the `BinLogStreamReader`.

When you set `use_column_name_cache=True`, the library will perform a query to the `INFORMATION_SCHEMA.COLUMNS` table to fetch the column names for a given table the first time it encounters an event for that table. The column names are then cached in memory for subsequent events for the same table, avoiding redundant queries.

This allows you to receive row data with column names as keys.

MySQL 8.0+ with `binlog_row_metadata=FULL`
------------------------------------------

In MySQL 8.0.1 and later, you can set `binlog_row_metadata` to `FULL` using `SET GLOBAL binlog_row_metadata = 'FULL'`. When this setting is enabled, the column names are included directly in the binlog events, and `use_column_name_cache` is not necessary.

Example
-------

Here is how to enable the column name cache when needed:

.. code-block:: python

    from pymysqlreplication import BinLogStreamReader

    mysql_settings = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': ''}

    # Enable the column name cache for MySQL 5.7 or MySQL 8.0+ with binlog_row_metadata=MINIMAL
    stream = BinLogStreamReader(
        connection_settings=mysql_settings,
        server_id=100,
        use_column_name_cache=True
    )

    for binlogevent in stream:
        if isinstance(binlogevent, WriteRowsEvent):
            # Now you can access values by column name
            user_id = binlogevent.rows[0]["values"]["id"]
            user_name = binlogevent.rows[0]["values"]["name"]
            print(f"New user: id={user_id}, name={user_name}")

    stream.close()

Important Considerations
------------------------

*   **Performance:** Enabling `use_column_name_cache` will result in an extra query to the database for each new table encountered in the binlog. The results are cached, so the performance impact should be minimal after the initial query for each table.
*   **Permissions:** The MySQL user used for replication must have `SELECT` privileges on the `INFORMATION_SCHEMA.COLUMNS` table.
*   **Default Behavior:** This feature is disabled by default (`use_column_name_cache=False`) to maintain backward compatibility and to avoid making extra queries unless explicitly requested.
