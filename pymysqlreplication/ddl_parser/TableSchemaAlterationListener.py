from typing import Dict

from MySqlParserListener import MySqlParserListener
from pymysqlreplication.table import Table
from pymysqlreplication.column import Column

class TableSchemaAlterationListener(MySqlParserListener):
    def __init__(self, table_map, schema):
        self.__schema: str = schema
        self.__table: str = None
        self.__table_map: Dict[int, Table] = table_map

    def enterTableName(self, ctx):
        self.__table = ctx.getText()

    def enterAlterByAddColumn(self, ctx):
        columm_name = ctx.uid(0).getText()
        column_type = ctx.columnDefinition().getText()

        table = self.__table_map[f"{self.__schema}.{self.__table}"]
        table.columns.append(Column(name=columm_name, column=column_type))

    def enterAlterByDropColumn(self, ctx):
        columm_name = ctx.uid(0).getText()

        table = self.__table_map[f"{self.__schema}.{self.__table}"]
        table.columns = [column for column in table.columns if column.name != columm_name]

    def enterAlterByModifyColumn(self, ctx):
        raise NotImplementedError()

    def enterAlterByRenameColumn(self, ctx):
        old_columm_name = ctx.uid(0).getText()
        new_columm_name = ctx.uid(1).getText()

        table = self.__table_map[f"{self.__schema}.{self.__table}"]
        for column in table.columns:
            if column.name == old_columm_name:
                column.name = new_columm_name
                break
