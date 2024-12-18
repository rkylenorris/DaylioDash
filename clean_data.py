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
        if self.name == 'customMoods':
            self.table['mood_value'] = 6 - self.table['mood_group_id']
            for mood in self.table[(self.table['mood_group_id'] in ([2, 3, 4])) &
                       (self.table['mood_group_order'] == 0)]:
                match mood['mood_group_id']:
                    case 2:
                        mood['custom_name'] = 'Good'
                    case 3:
                        mood['custom_name'] = 'Meh'
                    case 4:
                        mood['custom_name'] = 'Bad'

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

    @classmethod
    def create_mood_groups(cls, columns: list[ColumnInfo]):
        df = pd.DataFrame([
            {
                "id": 1,
                'name': 'The Best Days',
                'value': 5
            },
            {
                "id": 2,
                'name': 'The Good Days',
                'value': 4
            },
            {
                "id": 3,
                'name': 'The Meh Days',
                'value': 3
            },
            {
                "id": 4,
                'name': 'The Bad Days',
                'value': 2
            },
            {
                "id": 5,
                'name': 'The Worst Days',
                'value': 1
            },
        ])
        return DaylioTable('mood_groups', df, columns)
