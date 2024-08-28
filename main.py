import pandas as pd
import json
from pathlib import Path

data_dir = Path('data')
table_info_path = Path('table_info')

json_path = Path(data_dir / 'backup_2024_08_22.json')

with open(json_path, 'r') as f:
    data = json.load(f)

tables_needed = [
    'customMoods',
    'tags',
    'dayEntries',
    'tag_groups',
    'goalEntries'
]
dfs = []
for table in tables_needed:
    df = pd.read_excel(data_dir / f'table_info.xlsx', sheet_name=table)
    df.to_json(table_info_path / f'table_info_{table}.json', orient='records')



# for table in tables_needed:
#     print(table)
#     df = pd.DataFrame(data[table])
#     df.to_csv(data_dir / f'{table}.csv', index=False)
#     with open(data_dir / f'{table}_columns.txt', 'a') as f:
#         for column in df.columns:
#             f.write(column + '\n')
#     print("""
# -----------------------------------------------------------------------
#     """)
#
#
# combined_str = ""
# for file in data_dir.glob('*_columns.txt'):
#     table_name = file.stem.replace('_columns', '')
#     with open(file, 'r') as f:
#         table_columns = f.read()
#     table_info = f"{table_name}\n-------\n{table_columns}\n\n********************\n\n"
#     combined_str += table_info
#
# with open(data_dir / 'table_info.txt', 'w') as f:
#     f.write(combined_str)






# custom_moods_df = pd.DataFrame(data['customMoods'])
#
# custom_moods_df['createdAt'] = pd.to_datetime(custom_moods_df['createdAt'], unit='ms')
#
# # Display the DataFrame
# print(custom_moods_df.head())