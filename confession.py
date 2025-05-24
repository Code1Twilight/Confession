from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS confessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            to_name TEXT,
            message TEXT,
            song TEXT,
            sender TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    c.execute("SELECT to_name, message, song, date FROM confessions ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/submit', methods=['POST'])
def submit():
    to_name = request.form['to']
    message = request.form['message']
    song = request.form.get('song', '')
    sender = request.remote_addr
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    c.execute("INSERT INTO confessions (to_name, message, song, sender, date) VALUES (?, ?, ?, ?, ?)",
              (to_name, message, song, sender, date))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)