# DDL - data definition layer
import sqlite3

def create_table_users():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "users" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "email" TEXT NOT NULL UNIQUE,
            "password" TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()
