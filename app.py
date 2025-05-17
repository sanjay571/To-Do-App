from flask import Flask,render_template,request,redirect
import sqlite3
#start anew Flask web app
app = Flask(__name__)

# INITLIZE THE DATABASE
def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
             CREATE TABLE IF NOT EXISTS tasks(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   task TEXT NOT NULL,
                   complete BOOLEAN NOT NULL DEFAULT 0
                )
            ''')
    conn.commit() #save changes
    conn.close()  # close connection


# Display all tasks

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    cursor =conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall() #gets a list of all rows
    conn.close()
    return render_template('index.html',tasks=tasks)

# Add new task

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task) VALUES (?) ', (task,))
    conn.commit()
    conn.close()
    return redirect('/')

# Mark as complete
@app.route('/complete/<int:task_id>')
def complete(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET complete = 1 WHERE id = ?',(task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

#Delete task

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)