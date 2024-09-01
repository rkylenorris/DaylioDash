import pandas as pd
from typing import List
from table_info import DaylioTableInfo, InfoColumn


# TODO add method for merging with other daylio tables based on relationships values
# TODO move constructor stuff down to from_dataframe class method for it to work properly
class DaylioTable:
    def __init__(self, dataframe: pd.DataFrame, info: DaylioTableInfo):

        if info.name == 'customMoods':
            dataframe['mood_value'] = 6 - dataframe['mood_group_id']
        self.dataframe = dataframe
        self.name = info.name
        self.columns_info = info.columns
        self.relationships = info.relationships
        self.fix_timestamp_columns()

    def fix_timestamp_columns(self):
        last_col = InfoColumn('default', 'default', 'default')
        timestamp_cols = [x for x in self.columns_info if x.type_name == 'timestamp']
        for col in timestamp_cols:
            match col.name:
                case "createdAt":
                    col.field_to_create = "date"
                case "datetime":
                    col.field_to_create = "date"
                case "created_at":
                    col.field_to_create = "date"
                case "end_date":
                    col.field_to_create = "date_end"
                case _:
                    col.field_to_create = "none"
        for col in timestamp_cols:
            if col.field_to_create == 'none':
                continue
            else:
                self.dataframe[col.name] = self.dataframe[col.name].replace(0, pd.NaT)
                if self.name == "goals":
                    self.dataframe[col.name] = self.dataframe[col.name].replace(-1, pd.NaT)
                self.dataframe[col.name] = pd.to_datetime(self.dataframe[col.name], unit='ms')
                self.dataframe[col.field_to_create] = pd.to_datetime(self.dataframe[col.name].dt.date)



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
