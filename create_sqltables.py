import sqlite3
import prep
# Connect to SQLite database (or create it)
def create_daylio_sql_tables():
    conn = sqlite3.connect('data/daylio.db')
    cursor = conn.cursor()

    for tbl in prep.tables_needed:
        cursor.execute(f'DROP TABLE IF EXISTS {tbl}')
    cursor.execute(f'DROP TABLE IF EXISTS calendar')
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
        tags TEXT,
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
        DayOfYear INTEGER,
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

    conn.commit()
    conn.close()
