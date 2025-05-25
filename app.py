from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    priority TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

# Home Page with Search
@app.route('/')
def index():
    search = request.args.get('search', '')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if search:
        c.execute("SELECT * FROM tasks WHERE content LIKE ?", ('%' + search + '%',))
    else:
        c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks, search=search)

# Add Task
@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    priority = request.form['priority']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (content, priority) VALUES (?, ?)", (content, priority))
    conn.commit()
    conn.close()
    return redirect('/')

# Complete Task
@app.route('/complete/<int:id>')
def complete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Delete Task
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Edit Task
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    new_content = request.form.get('new_content')
    new_priority = request.form.get('new_priority')
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET content = ?, priority = ? WHERE id = ?", (new_content, new_priority, id))
        conn.commit()
        conn.close()
        return ('', 204)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
