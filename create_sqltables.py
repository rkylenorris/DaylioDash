import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('data/daylio.db')
cursor = conn.cursor()
cursor.close()

# Create customMoods table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customMoods (
    id INTEGER PRIMARY KEY,
    custom_name TEXT,
    mood_group_id INTEGER,
    mood_group_order INTEGER,
    createdAt DATETIME
)
''')

# Create tags table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name TEXT,
    createdAt DATETIME,
    `order` INTEGER,
    FOREIGN KEY id_tag_group REFERENCES tag_groups(id)
)
''')

# Create dayEntries table
cursor.execute('''
CREATE TABLE IF NOT EXISTS dayEntries (
    id INTEGER PRIMARY KEY,
    datetime DATETIME,
    FOREIGN KEY mood REFERENCES customMoods(id),
    note TEXT,
    note_title TEXT,
    tags TEXT
)
''')

# Create goalEntries table
cursor.execute('''
CREATE TABLE IF NOT EXISTS goalEntries (
    id INTEGER PRIMARY KEY,
    FOREIGN KEY goalid REFERENCES goals(goal_id),
    createdAt DATETIME,
)
''')

# Create goals table
cursor.execute('''
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY,
    goal_id INTEGER,
    createdAt DATETIME,
    FOREIGN KEY (id_tag) REFERENCES tags(id),
    end_date DATEIME,
    name TEXT,
    note TEXT
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
    name TEXT,
    createdAt DATETIME
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