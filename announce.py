from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('crisis.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        heading = request.form['heading']
        content = request.form['content']
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO submissions (heading, content) VALUES (?, ?)', (heading, content))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index')) 
    else:
        return render_template('announce.html')

if __name__ == '__main__':
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS submissions
                 (id INTEGER PRIMARY KEY, heading TEXT, content TEXT)''')
    conn.commit()
    conn.close()
    
    app.run(debug=True)
