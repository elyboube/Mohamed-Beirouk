import sqlite3
import os

db_path = 'tourism_platform/db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print('='*50)
    print('DATABASE TABLES:')
    print('='*50)
    for table in tables:
        print(f'  - {table[0]}')
    
    print('\n' + '='*50)
    print('TABLE RECORDS COUNT:')
    print('='*50)
    for table in tables:
        table_name = table[0]
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = cursor.fetchone()[0]
        print(f'  {table_name}: {count} records')
    
    conn.close()
else:
    print('Database file not found!')
