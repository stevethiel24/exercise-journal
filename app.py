from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

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
    date = request.form['date']
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
