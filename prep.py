import sys
import zipfile as zf
import pandas as pd
import os
import base64
from pathlib import Path
from datetime import datetime
import json

# TODO add code to archive source files after use

tables_needed = [
    'customMoods',
    'tags',
    'dayEntries',
    'goals',
    'prefs',
    'tag_groups',
    'goalEntries',
]


def is_weekend(day: int):
    if day > 5:
        return True
    else:
        return False


def is_weekday(day: int):
    if day < 6:
        return True
    else:
        return False


def create_calendar(start='2018-01-01', end=datetime.today().strftime('%Y-%m-%d')):
    df = pd.DataFrame({"TimeStamp": pd.date_range(start, end)})
    df['Date'] = pd.to_datetime(df['TimeStamp'])
    df["Day"] = df.TimeStamp.apply(lambda x: x.to_pydatetime().date().strftime('%w'))
    df["DayOfYear"] = df.TimeStamp.apply(lambda x: x.to_pydatetime().date().strftime('%-j'))
    df["DayName"] = df.TimeStamp.apply(lambda x: x.to_pydatetime().date().strftime('%A'))
    df["Week"] = df.Date.apply(lambda x: x.isocalendar()[1])
    df["Month"] = df.TimeStamp.apply(lambda x: x.to_pydatetime().date().strftime('%-m'))
    df["MonthName"] = df.TimeStamp.apply(lambda x: x.to_pydatetime().date().strftime('%B'))
    df["Quarter"] = df.TimeStamp.apply(lambda x: x.quarter)
    df["Year"] = df.TimeStamp.apply(lambda x: x.year)
    df['IsWeekend'] = df.Date.apply(lambda x: is_weekend(x.weekday()))
    df['IsWeekday'] = df.Date.apply(lambda x: is_weekday(x.weekday()))
    return df


def prep_backup():
    # create path for 'backup_%Y_%m_%d.daylio'
    file_name = datetime.today().strftime('backup_%Y_%m_%d.daylio')
    data_pickup_dir = Path(Path.home(), 'OneDrive/DaylioData')
    data_pickup_file = data_pickup_dir / file_name

    # check that working directory is correct
    expected_wd = "DaylioDash"

    print(Path.cwd())

    if Path.cwd().name != expected_wd:  # if wd not correct, search for dir in current user dir
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
    print('Unzipping daylio backup file..')
    with zf.ZipFile(str(data_pickup_file), 'r') as zip_ref:
        zip_ref.extractall(str(data_dir))
        os.remove(data_dir / "assets")

    with open(str(data_dir / "backup.daylio"), 'r') as d:
        contents = d.read()
        raw_json = base64.b64decode(contents).decode('utf-8')

    data = json.loads(raw_json)
    with open(Path(data_dir / "daylio.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
