import sqlite3

def create_table():
    conn = sqlite3.connect('telegram.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegran_id INTEGER NOT NULL,
            username TEXT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Llamar a la función
create_table()
