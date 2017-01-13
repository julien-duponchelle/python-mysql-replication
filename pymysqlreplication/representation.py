from pymysqlreplication.event import BinLogEvent, GtidEvent, RotateEvent, XidEvent, QueryEvent, BeginLoadQueryEvent, \
  ExecuteLoadQueryEvent, IntvarEvent
from pymysqlreplication.human_readable_representations import BinLogEventHumanReadableRepresentation, \
  GtidEventHumanReadableRepresentation, RotateEventHumanReadableRepresentation, XidEventHumanReadableRepresentation, \
  QueryEventHumanReadableRepresentation, BeginLoadQueryEventHumanReadableRepresentation, \
  ExecuteLoadQueryEventHumanReadableRepresentation, IntvarEventHumanReadableRepresentation, \
  RowsEventHumanReadableRepresentation, TableMapEventHumanRepresentation, UpdateRowsEventHumanRepresentation
from pymysqlreplication.json_representations import BinLogEventJsonRepresentation, GtidEventJsonRepresentation, \
  RotateEventJsonRepresentation, XidEventJsonRepresentation, QueryEventJsonRepresentation, \
  BeginLoadQueryEventJsonRepresentation, ExecuteLoadQueryEventJsonRepresentation, IntvarEventJsonRepresentation, \
  RowsEventJsonRepresentation, TableMapEventJsonRepresentation, UpdateRowsEventJsonRepresentation
from pymysqlreplication.row_event import DeleteRowsEvent, WriteRowsEvent, RowsEvent, TableMapEvent, UpdateRowsEvent

human_readable_mapping = {
  BinLogEvent: BinLogEventHumanReadableRepresentation,
  GtidEvent: GtidEventHumanReadableRepresentation,
  RotateEvent: RotateEventHumanReadableRepresentation,
  XidEvent: XidEventHumanReadableRepresentation,
  QueryEvent: QueryEventHumanReadableRepresentation,
  BeginLoadQueryEvent: BeginLoadQueryEventHumanReadableRepresentation,
  ExecuteLoadQueryEvent: ExecuteLoadQueryEventHumanReadableRepresentation,
  IntvarEvent: IntvarEventHumanReadableRepresentation,
  RowsEvent: RowsEventHumanReadableRepresentation,
  DeleteRowsEvent: RowsEventHumanReadableRepresentation,
  WriteRowsEvent: RowsEventHumanReadableRepresentation,
  TableMapEvent: TableMapEventHumanRepresentation,
  UpdateRowsEvent: UpdateRowsEventHumanRepresentation,
}

json_readable_mapping = {
  BinLogEvent: BinLogEventJsonRepresentation,
  GtidEvent: GtidEventJsonRepresentation,
  RotateEvent: RotateEventJsonRepresentation,
  XidEvent: XidEventJsonRepresentation,
  QueryEvent: QueryEventJsonRepresentation,
  BeginLoadQueryEvent: BeginLoadQueryEventJsonRepresentation,
  ExecuteLoadQueryEvent: ExecuteLoadQueryEventJsonRepresentation,
  IntvarEvent: IntvarEventJsonRepresentation,
  RowsEvent: RowsEventJsonRepresentation,
  DeleteRowsEvent: RowsEventJsonRepresentation,
  WriteRowsEvent: RowsEventJsonRepresentation,
  TableMapEvent: TableMapEventJsonRepresentation,
  UpdateRowsEvent: UpdateRowsEventJsonRepresentation,
}


class Readable(object):
  def __init__(self, representations):
    self.representations = representations

  def get_representation(self, event_class):
    rep = None
    try:
      rep = self.representations[event_class]
    except KeyError:
      pass
    return rep


class Human(object):
  def __init__(self):
    self.readable = Readable(human_readable_mapping)

  def get_representation(self, event_class):
    return self.readable.get_representation(event_class)


class Json(object):
  def __init__(self):
    self.readable = Readable(json_readable_mapping)

  def get_representation(self, event_class):
    return self.readable.get_representation(event_class)


string_to_types = {
  'HUMAN_READABLE': Human,
  'JSON': Json,
}
