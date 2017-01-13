import datetime


class BinLogEventHumanReadableRepresentation(object):
  def __init__(self, bin_log_event):
    self.event = bin_log_event

  def get_representation(self):
    return ("=== %s ===" % self.event.__class__.__name__ + "\n" +
            "Date: %s" % (datetime.datetime.fromtimestamp(self.event.timestamp).isoformat()) + "\n" +
            "Log position: %d" % self.event.packet.log_pos + "\n" +
            "Event size: %d" % self.event.event_size + "\n" +
            "Read bytes: %d" % self.event.packet.read_bytes)


class GtidEventHumanReadableRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return ("Commit: %s" % self.event.commit_flag + "\n" +
            "GTID_NEXT: %s" % self.event.gtid )


class RotateEventHumanReadableRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return ("=== %s ===" % self.event.__class__.__name__ + "\n" +
            "Position: %d" % self.event.position + "\n" +
            "Next binlog file: %s" % self.event.next_binlog)


class XidEventHumanReadableRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return "Transaction ID: %d" % self.event.xid


class QueryEventHumanReadableRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return ("Schema: %s" % self.event.schema + "\n" +
            "Execution time: %d" % self.event.execution_time + "\n" +
            "Query: %s" % self.event.query)


class BeginLoadQueryEventHumanReadableRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return ("File id: %d" % self.event.file_id + "\n" +
            "Block data: %s" % self.event.block_data)


class ExecuteLoadQueryEventHumanReadableRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return ("Slave proxy id: %d" % self.event.slave_proxy_id + "\n" +
            "Execution time: %d" % self.event.execution_time + "\n" +
            "Schema length: %d" % self.event.schema_length + "\n" +
            "Error code: %d" % self.event.error_code + "\n" +
            "Status vars length: %d" % self.event.status_vars_length + "\n" +
            "File id: %d" % self.event.file_id + "\n" +
            "Start pos: %d" % self.event.start_pos + "\n" +
            "End pos: %d" % self.event.end_pos + "\n" +
            "Dup handling flags: %d" % self.event.dup_handling_flags)


class IntvarEventHumanReadableRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return ("type: %d" % self.event.type + "\n" +
            "Value: %d" % self.event.value)


class BLAHEventHumanReadableRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return ("Table: %s.%s" % self.event.schema, self.event.table + "\n" +
            "Affected columns: %d" % self.event.number_of_columns + "\n" +
            "Changed rows: %d" % len(self.event.rows))


class RowsEventHumanReadableRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    rep = "Values:\n"
    for row in self.event.rows:
      rep += "--\n"
      for key in row["values"]:
        rep += "*" + key + ":" + row["values"][key] + "\n"
    return rep


class UpdateRowsEventHumanRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    rep = "Affected columns: %d" % self.event.number_of_columns + "\n"
    rep += "Values:" + "\n"
    for row in self.event.rows:
      rep += "--" + "\n"
      for key in row["before_values"]:
        rep += "*%s:%s=>%s" % (key,
                              row["before_values"][key],
                              row["after_values"][key]) + "\n"
    return rep

class TableMapEventHumanRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return ("Table id: %d" % self.event.table_id + "\n" +
            "Schema: %s" % self.event.schema + "\n" +
            "Table: %s" % self.event.table + "\n" +
            "Columns: %s" % self.event.column_count)