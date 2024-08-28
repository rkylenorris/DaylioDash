import json
from typing import List, Dict


class Column:
    def __init__(self, column: str, type_name: str, kind: str):
        self.column = column
        self.type_name = type_name
        self.kind = kind


class DaylioTable:
    def __init__(self, columns: List[Column], name: str):
        self.columns = columns
        self.name = name

    def get_columns_by_kind(self, kind: str) -> List[Column]:
        return [x for x in self.columns if x.kind == kind]

    def get_columns_by_name(self, name: str) -> List[Column]:
        return [x for x in self.columns if x.column == name]

    @classmethod
    def from_json(cls, json_data: str, table_name: str) -> 'DaylioTable':
        data = json.loads(json_data)
        columns = [Column(**item) for item in data]
        return cls(columns, table_name)


class DaylioTables:
    def __init__(self, daylio_tables: List[DaylioTable]):
        self.tables = daylio_tables

    def get_table(self, name: str) -> list[DaylioTable]:
        return [x for x in self.tables if x.name == name]
