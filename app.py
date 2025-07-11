from flask import Flask, render_template, request, redirect, url_for # type: ignore
import psycopg2 # type: ignore
import os
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS entries (
            id SERIAL PRIMARY KEY,
            date TEXT,
            exercise_type TEXT,
            duration INTEGER,
            distance REAL,
            notes TEXT
        )''')
        conn.commit()

@app.route('/')
def index():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM entries ORDER BY date DESC")
        entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date'] or datetime.today().strftime('%Y-%m-%d')
    exercise_type = request.form['exercise_type']
    duration = int(request.form['duration'])
    distance = float(request.form['distance'] or 0)
    notes = request.form['notes']

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('''INSERT INTO entries (date, exercise_type, duration, distance, notes)
                       VALUES (%s, %s, %s, %s, %s)''',
                    (date, exercise_type, duration, distance, notes))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM entries WHERE id = %s", (entry_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    if request.method == 'POST':
        date = request.form['date']
        exercise_type = request.form['exercise_type']
        duration = int(request.form['duration'])
        distance = float(request.form['distance'] or 0)
        notes = request.form['notes']

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('''UPDATE entries SET date=%s, exercise_type=%s, duration=%s,
                           distance=%s, notes=%s WHERE id=%s''',
                        (date, exercise_type, duration, distance, notes, entry_id))
            conn.commit()
        return redirect(url_for('index'))

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM entries WHERE id = %s", (entry_id,))
        entry = cur.fetchone()
    return render_template('edit.html', entry=entry)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
