import sys
import zipfile as zf
import pandas as pd
import json
import os
import base64
from pathlib import Path
from datetime import datetime
import json

# create path for 'backup_%Y_%m_%d.daylio'
date_string = datetime.today().strftime('backup_%Y_%m_%d.daylio')
data_pickup_dir = Path(Path.home(), 'OneDrive/DaylioData')
data_pickup_file = data_pickup_dir / date_string

# check that working directory is correct
expected_wd = "DaylioDash"

print(Path.cwd())

if Path.cwd().name != expected_wd: # if wd not correct, search for dir in current user dir
    for folder in Path.cwd().rglob(expected_wd):
        if folder.is_dir():
            os.chdir(str(folder))
            break
    else:
        print("directory 'DaylioDash' not found, terminating...")
        input("Press Enter to exit...")
        sys.exit("Unable to process; directory 'DaylioDash' not found.")

# create paths for data
data_dir = Path.cwd() / 'data'
# later add step to copy onedrive file to local dir before extracting
with zf.ZipFile(str(data_pickup_file), 'r') as zip_ref:
    zip_ref.extractall(str(data_dir))


with open(str(data_dir / "backup.daylio"), 'r') as d:
    contents = d.read()
    raw_json = base64.b64decode(contents).decode('utf-8')

data = json.loads(raw_json)
with open(Path(data_dir / "daylio.json"), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

tables_needed = [
    'customMoods',
    'tags',
    'dayEntries',
    'tag_groups',
    'goalEntries'
]