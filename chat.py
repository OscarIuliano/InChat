import sqlite3
from datetime import datetime

DB_NAME = "utenti.db"

def crea_tabella_messaggi():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messaggi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mittente TEXT NOT NULL,
            destinatario TEXT NOT NULL,
            testo TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def invia_messaggio(mittente, destinatario, testo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO messaggi (mittente, destinatario, testo, timestamp) VALUES (?, ?, ?, ?)",
              (mittente, destinatario, testo, timestamp))
    conn.commit()
    conn.close()

def leggi_chat(user1, user2):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT mittente, testo, timestamp FROM messaggi
        WHERE (mittente = ? AND destinatario = ?) OR
              (mittente = ? AND destinatario = ?)
        ORDER BY timestamp ASC
    """, (user1, user2, user2, user1))
    chat = c.fetchall()
    conn.close()
    return chat
