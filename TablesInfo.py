import json
from typing import List, Dict

class Column:
    def __init__(self, column: str, type_name: str, kind: str):
        self.column = column
        self.type_name = type_name
        self.kind = kind

class DaylioTable:
    def __init__(self, columns: List[Column]):
        self.columns = columns

    @classmethod
    def from_json(cls, json_data: str) -> 'DaylioTable':
        data = json.loads(json_data)
        columns = [Column(**item) for item in data]
        return cls(columns)

class DaylioTables:
    def __init__(self, daylio_tables: List[DaylioTable]):
        self.daylio_tables = daylio_tables