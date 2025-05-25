from flask import Flask, render_template, request, redirect
import pg8000
from datetime import datetime

app = Flask(__name__)

# PostgreSQL Database Config (Render details)
DB_HOST = 'dpg-d0p6k6euk2gs739baj2g-a.oregon-postgres.render.com'
DB_PORT = 5432
DB_NAME = 'confessionsdb'
DB_USER = 'confessionsdb_user'
DB_PASS = 'AyCjwE3ikc2pR9IkJIRyee3qUjMjlMW0'

# Helper function to connect to PostgreSQL
def get_db_connection():
    return pg8000.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# Initialize database
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS confessions (
            id SERIAL PRIMARY KEY,
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
    conn = get_db_connection()
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

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO confessions (to_name, message, song, font, style, date) VALUES (%s, %s, %s, %s, %s, %s)',
              (to, message, song, font, style, date))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
