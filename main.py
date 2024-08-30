import pandas as pd
import json
from pathlib import Path
import table_info as ti
import prep as pr

# TODO General Outline: prep file, load data into objects, create final datasets, create charts, export

# pr.prep_backup()

rolling_calendar = pr.create_calendar()
print(rolling_calendar.tail())
data_dir = Path('data')
table_info_path = Path('table_info')
relationships_dir = table_info_path / "relationships"

# load table info json
json_path = Path(data_dir / 'daylio.json')

with open(json_path, 'r', encoding='utf8') as f:
    data = json.loads(f.read())

info_tables_l = []

path = table_info_path / f'table_info.json'
table_info_str = path.read_text()
table_info_all = json.loads(table_info_str)

relationship_list = []
# load relationships info
for file in relationships_dir.iterdir():
    if file.is_file() and file.suffix == ".json":
        text = file.read_text()
        relationship_list.append(json.loads(text))

relationships = ti.Relationships(list(relationship_list))

for table in pr.tables_needed:

    info_tables_l.append(ti.DaylioTableInfo.from_json(table_info_all[table], table,
                                                      relationships.get_tables_relationships(table)))

info_tables = ti.DaylioInfoTables(info_tables_l)

print(info_tables.get_table('customMoods')[0].__dict__)


# for table in tables_needed:
#     print(table)
#     df = pd.DataFrame(data[table])
#     df.to_csv(data_dir / f'{table}.csv', index=False)






# custom_moods_df = pd.DataFrame(data['customMoods'])
#
# custom_moods_df['createdAt'] = pd.to_datetime(custom_moods_df['createdAt'], unit='ms')
#
# # Display the DataFrame
# print(custom_moods_df.head())