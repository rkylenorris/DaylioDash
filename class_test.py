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

# JSON data
json_data = '''
[
    {"Column":"id","TypeName":"Int64.Type","Kind":"number"},
    {"Column":"custom_name","TypeName":"Text.Type","Kind":"text"},
    {"Column":"mood_group_id","TypeName":"Int64.Type","Kind":"number"},
    {"Column":"mood_group_order","TypeName":"Int64.Type","Kind":"number"},
    {"Column":"createdAt","TypeName":"timestamp","Kind":"datetime"}
]
'''

# Create DaylioTable instance
daylio_table = DaylioTable.from_json(json_data)

# Print the columns to verify
for column in daylio_table.columns:
    print(f"Column: {column.column}, Type: {column.type_name}, Kind: {column.kind}")