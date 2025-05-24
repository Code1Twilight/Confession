from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS confessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            to_name TEXT,
            message TEXT,
            song TEXT,
            font TEXT,
            style TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    c.execute('SELECT to_name, message, song, font, style, date FROM confessions ORDER BY id DESC')
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/submit', methods=['POST'])
def submit():
    to = request.form.get('to')
    message = request.form.get('message')
    song = request.form.get('song')
    font = request.form.get('font')
    style = request.form.get('style')
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    c.execute('INSERT INTO confessions (to_name, message, song, font, style, date) VALUES (?, ?, ?, ?, ?, ?)',
              (to, message, song, font, style, date))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)(())
