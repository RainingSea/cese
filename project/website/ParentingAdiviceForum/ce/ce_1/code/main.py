from flask import Flask, render_template, request, redirect, url_for
from user import User
from thread import Thread
from advice import Advice
from contact_inquiry import ContactInquiry
import os

app = Flask(__name__)

def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_threads():
    threads = []
    if os.path.exists('threads.txt'):
        with open('threads.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                threads.append(Thread(title, content))
    return threads

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>')
def view_thread(thread_id):
    threads = load_threads()
    if 0 <= thread_id < len(threads):
        thread = threads[thread_id]
        return render_template('view_thread.html', thread=thread)
    return redirect(url_for('forum'))

@app.route('/post_advice')
def post_advice():
    return render_template('post_advice.html')

@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8183, debug=False)
