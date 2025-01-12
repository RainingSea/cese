from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# User class to handle user-related operations
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f'{self.username}|{self.password}\n')

# Thread class to represent forum threads
class Thread:
    def __init__(self, title, content, username):
        self.title = title
        self.content = content
        self.username = username

    def save(self):
        with open('threads.txt', 'a') as file:
            file.write(f'{self.title}|{self.content}|{self.username}\n')

# Comment class to represent comments on threads
class Comment:
    def __init__(self, thread_id, comment, username):
        self.thread_id = thread_id
        self.comment = comment
        self.username = username

    def save(self):
        with open('comments.txt', 'a') as file:
            file.write(f'{self.thread_id}|{self.comment}|{self.username}\n')

# Advice class to represent advice posts
class Advice:
    def __init__(self, title, content, username):
        self.title = title
        self.content = content
        self.username = username

    def save(self):
        with open('advice.txt', 'a') as file:
            file.write(f'{self.title}|{self.content}|{self.username}\n')

# ContactInquiry class to represent contact inquiries
class ContactInquiry:
    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    def save(self):
        with open('contact_inquiries.txt', 'a') as file:
            file.write(f'{self.name}|{self.email}|{self.message}\n')

# Load data from text files
def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    return users

def load_threads():
    threads = []
    if os.path.exists('threads.txt'):
        with open('threads.txt', 'r') as file:
            for line in file:
                title, content, username = line.strip().split('|')
                threads.append(Thread(title, content, username))
    return threads

def load_comments():
    comments = []
    if os.path.exists('comments.txt'):
        with open('comments.txt', 'r') as file:
            for line in file:
                thread_id, comment, username = line.strip().split('|')
                comments.append(Comment(int(thread_id), comment, username))
    return comments

def load_advice():
    advice_list = []
    if os.path.exists('advice.txt'):
        with open('advice.txt', 'r') as file:
            for line in file:
                title, content, username = line.strip().split('|')
                advice_list.append(Advice(title, content, username))
    return advice_list

def load_contact_inquiries():
    inquiries = []
    if os.path.exists('contact_inquiries.txt'):
        with open('contact_inquiries.txt', 'r') as file:
            for line in file:
                name, email, message = line.strip().split('|')
                inquiries.append(ContactInquiry(name, email, message))
    return inquiries

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/forum')
def forum():
    threads = load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>')
def view_thread(thread_id):
    threads = load_threads()
    comments = load_comments()
    if thread_id < len(threads):
        thread = threads[thread_id]
        thread_comments = [c for c in comments if c.thread_id == thread_id]
        return render_template('view_thread.html', thread=thread, comments=thread_comments)
    return redirect(url_for('forum'))

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session.get('username')  # Assuming user is logged in
        advice = Advice(title, content, username)
        advice.save()
        return redirect(url_for('home'))
    return render_template('post_advice.html')

@app.route('/my_account')
def my_account():
    if 'username' in session:
        return render_template('my_account.html')
    return redirect(url_for('login'))

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        inquiry = ContactInquiry(name, email, message)
        inquiry.save()
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8310, debug=False)
