import pandas as pd
import json
from pathlib import Path
import table_info as ti
import prep as pr
import daylio_tables as dyt
import sqlite3
from create_sqltables import create_daylio_sql_tables
from sql_tools import execute_command_script

# TODO General Outline: prep file, load data into objects, create final datasets, create charts, export

# pr.prep_backup()

rolling_calendar = pr.create_calendar()

print(rolling_calendar.tail())
data_dir = Path('data')
rolling_calendar.to_csv(data_dir / 'calendar.csv', index=False)
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
all_tables = []
for info_table in info_tables.tables:
    tbl_name = info_table.name
    csv_path = data_dir / f'{tbl_name}.csv'
    all_tables.append(dyt.DaylioTable(pd.read_csv(csv_path), info_table))

create_daylio_sql_tables()

conn = sqlite3.connect('data/daylio.db')

for daylio_table in all_tables:

    if daylio_table.name in ['prefs']:
        continue

    print(f"Loading table {daylio_table.name} to daylio.db using sqlite")

    info_tbl = info_tables.get_table(daylio_table.name)
    cols_to_use = info_tbl[0].get_columns_names()
    daylio_table.dataframe[cols_to_use].to_sql(daylio_table.name, con=conn, if_exists='append', index=False)

rolling_calendar.to_sql('calendar', con=conn, if_exists='append', index=False)
# TODO need to write sql queries to provide final report views aggregating data
# TODO create sql functions for running those queries and returning the dfs
# TODO convert those views into charts and graphs using Plotly
conn.commit()

execute_command_script(conn, 'create_entry_tags.sql')