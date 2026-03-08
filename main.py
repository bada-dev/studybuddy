import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

def get_db():
    conn = sqlite3.connect('leaderboard.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        total_minutes INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        reborns INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-password', methods=['POST'])
def check_password():
    data = request.get_json()
    if data.get('password') == ADMIN_PASSWORD:
        return jsonify({'correct': True})
    return jsonify({'correct': False})

@app.route('/set-username', methods=['POST'])
def set_username():
    data = request.get_json()
    username = data.get('username', '').strip()
    if not username or len(username) > 20:
        return jsonify({'success': False, 'error': 'Invalid username'})
    conn = get_db()
    try:
        conn.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
        conn.commit()
        return jsonify({'success': True})
    finally:
        conn.close()

@app.route('/sync-score', methods=['POST'])
def sync_score():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'success': False})
    total_minutes = data.get('totalMinutes', 0)
    streak = data.get('streak', 0)
    reborns = data.get('reborns', 0)
    conn = get_db()
    conn.execute('''INSERT INTO users (username, total_minutes, streak, reborns)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(username) DO UPDATE SET
                    total_minutes=excluded.total_minutes,
                    streak=excluded.streak,
                    reborns=excluded.reborns''',
                 (username, total_minutes, streak, reborns))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/leaderboard')
def leaderboard():
    conn = get_db()
    users = conn.execute(
        'SELECT username, total_minutes, streak, reborns FROM users ORDER BY total_minutes DESC LIMIT 20'
    ).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

if __name__ == '__main__':
    app.run()
