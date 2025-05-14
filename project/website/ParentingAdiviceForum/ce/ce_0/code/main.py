from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self):
        self.users_file = 'users.txt'
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def register(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                if line.startswith(username + '|'):
                    return False
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class ThreadManager:
    def __init__(self):
        self.threads_file = 'threads.txt'
        if not os.path.exists(self.threads_file):
            open(self.threads_file, 'w').close()

    def create_thread(self, title, content, author):
        thread_id = str(int(datetime.now().timestamp()))
        with open(self.threads_file, 'a') as f:
            f.write(f"{thread_id}|{title}|{content}|{author}|{datetime.utcnow()}\n")
        return True

    def get_threads(self):
        threads = []
        with open(self.threads_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                threads.append({
                    'id': parts[0],
                    'title': parts[1],
                    'author': parts[3],
                    'timestamp': parts[4]
                })
        return threads

    def get_thread_details(self, thread_id):
        with open(self.threads_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == thread_id:
                    return {
                        'id': parts[0],
                        'title': parts[1],
                        'content': parts[2],
                        'author': parts[3],
                        'timestamp': parts[4]
                    }
        return None

class CommentManager:
    def __init__(self):
        self.comments_file = 'comments.txt'
        if not os.path.exists(self.comments_file):
            open(self.comments_file, 'w').close()

    def add_comment(self, thread_id, content, author):
        comment_id = str(int(datetime.now().timestamp()))
        with open(self.comments_file, 'a') as f:
            f.write(f"{comment_id}|{thread_id}|{content}|{author}|{datetime.utcnow()}\n")
        return True

    def get_comments(self, thread_id):
        comments = []
        with open(self.comments_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[1] == thread_id:
                    comments.append({
                        'id': parts[0],
                        'content': parts[2],
                        'author': parts[3],
                        'timestamp': parts[4]
                    })
        return comments

class AdviceManager:
    def __init__(self):
        self.advice_file = 'advice.txt'
        if not os.path.exists(self.advice_file):
            open(self.advice_file, 'w').close()

    def post_advice(self, title, content, author):
        advice_id = str(int(datetime.now().timestamp()))
        with open(self.advice_file, 'a') as f:
            f.write(f"{advice_id}|{title}|{content}|{author}|{datetime.utcnow()}\n")
        return True

    def get_advice(self):
        advice = []
        with open(self.advice_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                advice.append({
                    'id': parts[0],
                    'title': parts[1],
                    'content': parts[2],
                    'author': parts[3],
                    'timestamp': parts[4]
                })
        return advice

class ContactManager:
    def __init__(self):
        self.contacts_file = 'contacts.txt'
        if not os.path.exists(self.contacts_file):
            open(self.contacts_file, 'w').close()

    def submit_contact(self, name, email, message):
        contact_id = str(int(datetime.now().timestamp()))
        with open(self.contacts_file, 'a') as f:
            f.write(f"{contact_id}|{name}|{email}|{message}|{datetime.utcnow()}\n")
        return True

user_manager = UserManager()
thread_manager = ThreadManager()
comment_manager = CommentManager()
advice_manager = AdviceManager()
contact_manager = ContactManager()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/forum')
def forum():
    if 'username' not in session:
        return redirect(url_for('login'))
    threads = thread_manager.get_threads()
    return render_template('forum.html', threads=threads)

@app.route('/thread/<thread_id>')
def view_thread(thread_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    thread = thread_manager.get_thread_details(thread_id)
    comments = comment_manager.get_comments(thread_id)
    return render_template('view_thread.html', thread=thread, comments=comments)

@app.route('/new_thread', methods=['POST'])
def new_thread():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    content = request.form['content']
    thread_manager.create_thread(title, content, session['username'])
    return redirect(url_for('forum'))

@app.route('/add_comment/<thread_id>', methods=['POST'])
def add_comment(thread_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    content = request.form['comment']
    comment_manager.add_comment(thread_id, content, session['username'])
    return redirect(url_for('view_thread', thread_id=thread_id))

@app.route('/advice')
def advice():
    if 'username' not in session:
        return redirect(url_for('login'))
    advice_list = advice_manager.get_advice()
    return render_template('post_advice.html', advice=advice_list)

@app.route('/post_advice', methods=['POST'])
def post_advice():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    content = request.form['content']
    advice_manager.post_advice(title, content, session['username'])
    return redirect(url_for('advice'))

@app.route('/account')
def account():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('my_account.html', username=session['username'])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact_manager.submit_contact(name, email, message)
        return render_template('contact.html', message='Thank you for your message!')
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8121, debug=False)
