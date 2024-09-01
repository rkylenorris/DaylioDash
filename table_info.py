from typing import List, Dict

# TODO create txt file basis for table relationships


class Relationship:
    def __init__(self, name: str, left_table: str, left_column: str, right_table: str, right_column: str):
        self.name = name
        self.left_table = left_table
        self.left_column = left_column
        self.right_table = right_table
        self.right_column = right_column


class Relationships:
    def __init__(self, relationships: List[Relationship]):
        self.relationships = relationships

    def get_tables_relationships(self, table_name: str) -> List[Relationship]:
        # relationship name has both tables in it, so this is quicker than check right and left able attributes
        return [x for x in self.relationships if table_name in x['name']]


    def get_relationship(self, relationship_name: str) -> Relationship:
        for relationship in self.relationships:
            if relationship['name'] == relationship_name:
                return relationship


class InfoColumn:
    def __init__(self, name: str, type_name: str, kind: str):
        self.name = name
        self.type_name = type_name
        self.kind = kind


class DaylioTableInfo:
    def __init__(self, columns: List[InfoColumn], name: str, relationships: Relationships):
        self.columns = columns
        self.name = name
        self.relationships = relationships

    def get_columns_names(self) -> List[str]:
        columns_names = []
        for column in self.columns:
            columns_names.append(column.name)
        return columns_names

    def get_columns_by_type_name(self, type_name: str) -> List[InfoColumn]:
        return [x for x in self.columns if x.type_name == type_name]

    def get_columns_by_name(self, name: str) -> List[InfoColumn]:
        return [x for x in self.columns if x.name == name]

    @classmethod
    def from_json(cls, json_data: Dict, table_name: str, relationships: List[Relationship]) -> 'DaylioTableInfo':
        data = json_data
        columns = [InfoColumn(**item) for item in data]
        return cls(columns, table_name, relationships)


class DaylioInfoTables:
    def __init__(self, daylio_tables: List[DaylioTableInfo]):
        self.tables = daylio_tables

    def get_table(self, name: str) -> list[DaylioTableInfo]:
        return [x for x in self.tables if x.name == name]
