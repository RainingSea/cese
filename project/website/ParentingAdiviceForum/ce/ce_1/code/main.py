from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load data from text files
def load_users():
    users = []
    with open('users.txt', 'r') as f:
        for line in f:
            users.append(line.strip().split('|'))
    return users

def load_threads():
    threads = []
    with open('threads.txt', 'r') as f:
        for line in f:
            threads.append(line.strip().split('|'))
    return threads

def load_comments():
    comments = []
    with open('comments.txt', 'r') as f:
        for line in f:
            comments.append(line.strip().split('|'))
    return comments

def load_contact_inquiries():
    inquiries = []
    with open('contact_inquiries.txt', 'r') as f:
        for line in f:
            inquiries.append(line.strip().split('|'))
    return inquiries

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    threads = load_threads()
    thread = threads[thread_id]
    comments = load_comments()
    if request.method == 'POST':
        content = request.form['content']
        with open('comments.txt', 'a') as f:
            f.write(f"{thread[0]}|{content}\n")
        return redirect(url_for('view_thread', thread_id=thread_id))
    return render_template('view_thread.html', thread=thread, comments=comments)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with open('threads.txt', 'a') as f:
            f.write(f"{title}|{content}\n")
        return redirect(url_for('forum'))
    return render_template('post_advice.html')

@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with open('contact_inquiries.txt', 'a') as f:
            f.write(f"{name}|{email}|{message}\n")
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8104, debug=False)
