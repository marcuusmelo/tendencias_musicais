import sqlite3

def get_db_connection():
    conn = sqlite3.connect('/Users/marcusmelo/Desktop/projeto_m4_gh/tendencias_musicais_web/db.sqlite3')
    conn.text_factory = str

    return conn
