import datetime
import json


class BinLogEventJsonRepresentation(object):
  def __init__(self, bin_log_event):
    self.event = bin_log_event

  def get_representation(self):
    return json.dumps({"event": self.event.__class__.__name__,
                       "date": (datetime.datetime.fromtimestamp(self.event.timestamp).isoformat()),
                       "log_position": self.event.packet.log_pos,
                       "event_size": self.event.event_size,
                       "ready_bytes": self.event.packet.read_bytes})


class GtidEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return json.dumps({"commit":self.event.commit_flag,
                      "gtid_next": self.event.gtid})


class RotateEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return json.dumps({"name" : self.event.__class__.__name__ ,
                      "position" : self.event.position,
                      "next_binlog_file": self.event.next_binlog})


class XidEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return json.dumps({"transaction_id": self.event.xid})


class QueryEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return json.dumps({"schema": self.event.schema,
                      "execution_time": self.event.execution_time,
                      "query": self.event.query})


class BeginLoadQueryEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return json.dumps({"file_id": self.event.file_id,
                      "block_data": self.event.block_data})


class ExecuteLoadQueryEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return json.dumps({"slave_proxy_id": self.event.slave_proxy_id,
                       "execution_time": self.event.execution_time,
                       "Schema_length": self.event.schema_length,
                       "error_code": self.event.error_code,
                       "status_vars_length": self.event.status_vars_length,
                       "file_id": self.event.file_id,
                       "start_pos": self.event.start_pos,
                       "end_pos": self.event.end_pos,
                       "dup_handling_flags": self.event.dup_handling_flags})


class IntvarEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return json.dumps({"type": self.event.type,
                       "value": self.event.value})


class RowsEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event

  def get_representation(self):
    return json.dumps({"values": self.event.rows})
  

class TableMapEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event
  
  def get_representation(self):
    return {"table_id": self.event.table_id,
            "schema": self.event.schema,
            "table": self.event.table,
            "columns": self.event.column_count}


class UpdateRowsEventJsonRepresentation(object):
  def __init__(self, event):
    self.event = event
