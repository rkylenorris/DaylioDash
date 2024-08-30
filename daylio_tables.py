import pandas as pd
from typing import List
from table_info import DaylioTableInfo


fields_to_convert_to_datetime = [
    'createdAt',
    'datetime'
]


# TODO add method for merging with other daylio tables based on relationships values
class DaylioTable:
    def __init__(self, dataframe: pd.DataFrame, info: DaylioTableInfo):
        for column in dataframe.columns:
            if column in fields_to_convert_to_datetime:
                dataframe[column] = pd.to_datetime(dataframe[column], unit='ms')
        self.dataframe = dataframe
        self.name = info.name
        self.columns_info = info.columns
        self.relationships = info.relationships

    @classmethod
    def from_dataframe(cls, dataframe: pd.DataFrame, info: DaylioTableInfo) -> 'DaylioTable':
        return cls(dataframe, info)

    def get_column(self, column_name: str) -> pd.Series:
        """Return a specific column as a pandas Series."""
        if column_name in self.dataframe.columns:
            return self.dataframe[column_name]
        else:
            raise KeyError(f"Column {column_name} does not exist in the table.")

    def filter_by_column_value(self, column_name: str, value) -> pd.DataFrame:
        """Filter the DataFrame by a specific column's value."""
        if column_name in self.dataframe.columns:
            return self.dataframe[self.dataframe[column_name] == value]
        else:
            raise KeyError(f"Column {column_name} does not exist in the table.")

    def add_column(self, column_name: str, data: List) -> None:
        """Add a new column to the DataFrame."""
        self.dataframe[column_name] = data

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the class back to a pandas DataFrame."""
        return self.dataframe

    def to_json(self) -> str:
        """Convert the DataFrame to JSON format."""
        return self.dataframe.to_json()

    def __repr__(self):
        return f"DaylioTable(name={self.name}, dataframe=\n{self.dataframe})"
