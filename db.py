import sqlite3
from datetime import datetime

DB_PATH = 'reviews.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_review(text, sentiment):
    created_at = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)', (text, sentiment, created_at))
    review_id = c.lastrowid
    conn.commit()
    conn.close()
    return {'id': review_id, 'text': text, 'sentiment': sentiment, 'created_at': created_at}

def get_reviews(sentiment=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if sentiment:
        c.execute('SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ?', (sentiment,))
    else:
        c.execute('SELECT id, text, sentiment, created_at FROM reviews')
    rows = c.fetchall()
    conn.close()
    return [
        {'id': row[0], 'text': row[1], 'sentiment': row[2], 'created_at': row[3]}
        for row in rows
    ] 