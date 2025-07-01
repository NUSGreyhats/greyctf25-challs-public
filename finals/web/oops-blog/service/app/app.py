from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random
import base64
import socket

ADMIN_HOST = "web-oops-admin"
ADMIN_PORT = 3001

app = Flask(__name__)


@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'none'; object-src 'none'; base-uri 'none'; style-src 'self'; script-src 'self' 'unsafe-eval'; font-src 'self';"
    return response


# Database setup
def init_db():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  body TEXT NOT NULL,
                  short_code TEXT UNIQUE NOT NULL,
                  clicks INTEGER DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_db_connection():
    conn = sqlite3.connect('posts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    post_url = None
    
    if request.method == 'POST':
        body = request.form['body']

        
        # Generate unique short code
        while True:
            short_code = generate_short_code()
            conn = get_db_connection()
            existing = conn.execute('SELECT id FROM posts WHERE short_code = ?', 
                                  (short_code,)).fetchone()
            if not existing:
                break
            conn.close()
        
        # Save to database
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (body, short_code) VALUES (?, ?)',
                    (body, short_code))
        conn.commit()
        conn.close()
        
        post_url = request.host_url + short_code
        message = "Post created successfully!"
    
    return render_template("index.html", 
                                message=message, 
                                post_url=post_url)

@app.post('/report')
def report():
    submit_id = request.form["submit_id"]
    submit_id = submit_id.split("/")[-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADMIN_HOST, ADMIN_PORT))
    s.sendall(submit_id.encode())
    s.close()
    return render_template("index.html", 
                                report_message="Reported successfully.")


@app.route('/<short_code>')
def render_post(short_code):
    conn = get_db_connection()
    post = conn.execute('SELECT body FROM posts WHERE short_code = ?', 
                           (short_code,)).fetchone()
    conn.close()
    
    if post:
        return render_template("post.html", body=base64.b64encode(post["body"].encode()).decode()), 200
    else:
        return redirect("/")

init_db()
