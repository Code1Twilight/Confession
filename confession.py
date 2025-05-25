from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# PostgreSQL connection from Render environment variable
DATABASE_URL = "postgresql://confessionsdb_user:AyCjwE3ikc2pR9IkJIRyee3qUjMjlMW0@dpg-d0p6k6euk2gs739baj2g-a.oregon-postgres.render.com/confessionsdb"

# Fix for SQLAlchemy deprecation warnings (optional but recommended)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLAlchemy setup
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Confession model
class Confession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_name = db.Column(db.String(100))
    message = db.Column(db.Text)
    song = db.Column(db.String(200))
    font = db.Column(db.String(50))
    style = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    posts = Confession.query.order_by(Confession.id.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/submit', methods=['POST'])
def submit():
    to = request.form.get('to')
    message = request.form.get('message')
    song = request.form.get('song')
    font = request.form.get('font')
    style = request.form.get('style')

    new_confession = Confession(
        to_name=to,
        message=message,
        song=song,
        font=font,
        style=style
    )
    db.session.add(new_confession)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created.")
    app.run(debug=True)
