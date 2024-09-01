
def execute_command_script(connection, script_path):
    with open(script_path, 'r') as s:
        script = s.read()
    cursor = connection.cursor()
    cursor.executescript(script)
    connection.commit()
    connection.close()
