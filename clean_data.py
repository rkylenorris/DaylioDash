import pandas as pd


class ColumnInfo:

    def __init__(self, name: str, type_name: str, kind: str):
        self.name = name
        self.type_name = type_name
        self.kind = kind


class DaylioTable:

    def __init__(self, name: str, df: pd.DataFrame, columns: list[ColumnInfo]):
        self.name = name
        self.table = df
        self.column_info = columns
        self.__fix_dates()

    def __fix_dates(self):
        field_to_create = "none"
        for col in [x for x in self.column_info if x.type_name == 'timestamp']:
            match col.name:
                case 'createdAt' | "datetime" | "created_at":
                    field_to_create = "date"
                case 'end_date':
                    field_to_create = 'date_end'
                case _:
                    field_to_create = 'none'
            if field_to_create == 'none':
                continue
            else:
                self.table[col.name] = self.table[col.name].replace(0, pd.NaT)
                if self.name == 'goals':
                    self.table[col.name] = self.table[col.name].replace(-1, pd.NaT)
                self.table[col.name] = pd.to_datetime(self.table[col.name], unit='ms')
                self.table[field_to_create] = pd.to_datetime(self.table[col.name].dt.date)

    def to_sql(self, connection):
        cols = [x.name for x in self.column_info]
        self.table[cols].to_sql(self.name, connection, if_exists='replace', index=False)