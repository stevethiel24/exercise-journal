from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = 'exercise.db'

# Ensure the database and table exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    exercise_type TEXT,
                    duration INTEGER,
                    distance REAL,
                    notes TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM entries ORDER BY date DESC")
    entries = c.fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date'] or datetime.today().strftime('%Y-%m-%d')
    exercise_type = request.form['exercise_type']
    duration = int(request.form['duration'])
    distance = float(request.form['distance'] or 0)
    notes = request.form['notes']

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO entries (date, exercise_type, duration, distance, notes) VALUES (?, ?, ?, ?, ?)",
              (date, exercise_type, duration, distance, notes))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
