from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("notes.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect("notes.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = cur.fetchall()

    conn.close()

    return render_template("index.html", notes=notes)

@app.route("/add_note", methods=["POST"])
def add_note():
    data = request.get_json()
    note = data["note"]

    conn = sqlite3.connect("notes.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes(content) VALUES(?)",
        (note,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note Saved Successfully"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)