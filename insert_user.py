import sqlite3

def insert_user(telegram_id, username):
    conn = sqlite3.connect('telegram.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (telegran_id, username)
        VALUES (?, ?)
    ''', (telegram_id, username))
    conn.commit()
    cursor.close()
    conn.close()
