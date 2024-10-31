import sqlite3
import prep
from datetime import datetime
# Connect to SQLite database (or create it)


def create_daylio_sql_tables():
    conn = sqlite3.connect('data/daylio.db')
    cursor = conn.cursor()

    for tbl in prep.tables_needed:
        cursor.execute(f'DROP TABLE IF EXISTS {tbl}')
    cursor.execute('DROP TABLE IF EXISTS calendar')
    cursor.execute('DROP TABLE IF EXISTS mood_groups')
    cursor.execute('DROP TABLE IF EXISTS entry_tags')
    # Create customMoods table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customMoods (
        id INTEGER PRIMARY KEY,
        custom_name TEXT,
        mood_value INTEGER,
        mood_group_id INTEGER,
        mood_group_order INTEGER,
        createdAt DATETIME,
        date DATE
    )
    ''')

    # Create tags table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY,
        name TEXT,
        createdAt DATETIME,
        `order` INTEGER,
        id_tag_group INTEGER,
        date DATE,
        FOREIGN KEY (id_tag_group) REFERENCES tag_groups(id)
    )
    ''')

    # Create dayEntries table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dayEntries (
        id INTEGER PRIMARY KEY,
        datetime DATETIME,
        mood INTEGER,
        note TEXT,
        note_title TEXT,
        date DATE,
        FOREIGN KEY (mood) REFERENCES customMoods(id)
    )
    ''')

    # Create goalEntries table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goalEntries (
        id INTEGER PRIMARY KEY,
        goalId INTEGER,
        createdAt DATETIME,
        date DATE,
        FOREIGN KEY (goalId) REFERENCES goals(goal_id)
    )
    ''')

    # Create goals table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY,
        goal_id INTEGER,
        created_at DATETIME,
        id_tag INTEGER,
        end_date DATEIME,
        name TEXT,
        note TEXT,
        date DATE,
        date_end Date,
        FOREIGN KEY (id_tag) REFERENCES tags(id)
    )
    ''')

    # Create prefs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prefs (
        AUTO_BACKUP_IS_ON BOOLEAN,
        LAST_DAYS_IN_ROWS_NUMBER INTEGER,
        DAYS_IN_ROW_LONGEST_CHAIN INTERGER,
        LAST_ENTRY_CREATION_TIME DATETIME
    )
    ''')

    # Create tag_groups table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tag_groups (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
    ''')

    # create calendar table
    cursor.execute('''
    CREATE TABLE calendar (
        TimeStamp DATETIME PRIMARY KEY,
        Date DATE,
        Day INTEGER,
        DayName TEXT,
        Week INTEGER,
        Month INTEGER,
        MonthName TEXT,
        Quarter INTEGER,
        Year INTEGER,
        IsWeekend BOOLEAN,
        IsWeekday BOOLEAN
    );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_groups (
            id INTEGER PRIMARY KEY,
            name TEXT,
            value INTEGER
        
        );
        ''')

    cursor.execute('''
    CREATE TABLE entry_tags (
    entry_id INTEGER,
    tag TEXT,
    FOREIGN KEY (entry_id) REFERENCES dayEntries(id)
);
    ''')
    conn.commit()
    conn.close()


def insert_mood_groups():
    conn = sqlite3.connect('data/daylio.db')
    cursor = conn.cursor()
    mood_grps = [
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
    ]
    select_query = '''
    INSERT INTO mood_groups (id, name, value)
    VALUES (?, ?, ?)
    '''
    for grp in mood_grps:
        cursor.execute(select_query, (grp['id'], grp['name'], grp['value']))

    conn.commit()
    conn.close()


def insert_prefs(prefs_dict):
    conn = sqlite3.connect('data/daylio.db')
    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO prefs 
    (AUTO_BACKUP_IS_ON, LAST_DAYS_IN_ROWS_NUMBER, DAYS_IN_ROW_LONGEST_CHAIN, LAST_ENTRY_CREATION_TIME) 
    VALUES (?, ?, ?, ?)
    '''
    bckup = next(filter(lambda x: x['key'] == 'AUTO_BACKUP_IS_ON', prefs_dict))['value']
    last_days_inarow = next(filter(lambda x: x['key'] == 'LAST_DAYS_IN_ROWS_NUMBER', prefs_dict))['value']
    longest_days_inarow = next(filter(lambda x: x['key'] == 'DAYS_IN_ROW_LONGEST_CHAIN', prefs_dict))['value']
    last_entry_time = next(filter(lambda x: x['key'] == 'LAST_ENTRY_CREATION_TIME', prefs_dict))['value']
    last_entry_time = datetime.fromtimestamp(last_entry_time/1000)
    vals = [bckup, last_days_inarow, longest_days_inarow, last_entry_time]
    cursor.execute(insert_query, vals)
    conn.commit()
    conn.close()
