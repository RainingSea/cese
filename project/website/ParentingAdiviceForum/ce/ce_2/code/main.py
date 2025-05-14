from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

class FileStorage:
    @staticmethod
    def read_data(file):
        try:
            with open(file, 'r') as f:
                return [line.strip().split('|') for line in f.readlines()]
        except FileNotFoundError:
            return []

    @staticmethod
    def write_data(file, data):
        try:
            with open(file, 'w') as f:
                for record in data:
                    f.write('|'.join(record) + '\n')
            return True
        except:
            return False

    @staticmethod
    def append_data(file, record):
        try:
            with open(file, 'a') as f:
                f.write('|'.join(record) + '\n')
            return True
        except:
            return False

class ParentingForum:
    def __init__(self):
        self.storage = FileStorage()

    def login(self, username, password):
        users = self.storage.read_data('users.txt')
        for user in users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username, password):
        users = self.storage.read_data('users.txt')
        for user in users:
            if user[0] == username:
                return False
        return self.storage.append_data('users.txt', [username, password])

    def create_thread(self, title, content, author):
        threads = self.storage.read_data('threads.txt')
        thread_id = str(int(time.time()))
        return self.storage.append_data('threads.txt', 
            [thread_id, title, content, author, time.strftime('%Y-%m-%d %H:%M')])

    def add_comment(self, thread_id, content, author):
        comments = self.storage.read_data('comments.txt')
        comment_id = str(int(time.time()))
        return self.storage.append_data('comments.txt', 
            [comment_id, thread_id, content, author, time.strftime('%Y-%m-%d %H:%M')])

    def post_advice(self, title, content, author):
        advice = self.storage.read_data('advice.txt')
        post_id = str(int(time.time()))
        return self.storage.append_data('advice.txt', 
            [post_id, title, content, author, time.strftime('%Y-%m-%d %H:%M')])

    def update_profile(self, username, new_data):
        users = self.storage.read_data('users.txt')
        updated = False
        for i, user in enumerate(users):
            if user[0] == username:
                users[i] = [username, new_data['password']]
                updated = True
                break
        if updated:
            return self.storage.write_data('users.txt', users)
        return False

    def delete_account(self, username):
        users = self.storage.read_data('users.txt')
        users = [user for user in users if user[0] != username]
        return self.storage.write_data('users.txt', users)

    def contact_admin(self, name, email, message):
        return self.storage.append_data('contacts.txt', 
            [name, email, message, time.strftime('%Y-%m-%d %H:%M')])

forum = ParentingForum()

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
        if forum.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if forum.register(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/forum')
def forum_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    threads = forum.storage.read_data('threads.txt')
    return render_template('forum.html', threads=threads)

@app.route('/thread/<thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    threads = forum.storage.read_data('threads.txt')
    thread = None
    for t in threads:
        if t[0] == thread_id:
            thread = t
            break
    
    if request.method == 'POST':
        content = request.form['content']
        forum.add_comment(thread_id, content, session['username'])
    
    comments = [c for c in forum.storage.read_data('comments.txt') if c[1] == thread_id]
    return render_template('view_thread.html', thread=thread, comments=comments)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if forum.post_advice(title, content, session['username']):
            return redirect(url_for('forum_page'))
    
    return render_template('post_advice.html')

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        if forum.update_profile(session['username'], {'password': new_password}):
            return redirect(url_for('home'))
    
    return render_template('my_account.html', username=session['username'])

@app.route('/delete_account')
def delete_account():
    if 'username' in session:
        username = session['username']
        forum.delete_account(username)
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        if forum.contact_admin(name, email, message):
            return redirect(url_for('home'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8123, debug=False)
