from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from thread import Thread
from comment import Comment
from contact_inquiry import ContactInquiry

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        print("User file not found.")
    return users

def load_threads():
    threads = []
    try:
        with open('threads.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                threads.append(Thread(title, content))
    except FileNotFoundError:
        print("Threads file not found.")
    return threads

def load_comments():
    comments = []
    try:
        with open('comments.txt', 'r') as file:
            for line in file:
                thread_id, content = line.strip().split('|')
                comments.append(Comment(int(thread_id), content))
    except FileNotFoundError:
        print("Comments file not found.")
    return comments

def load_contact_inquiries():
    inquiries = []
    try:
        with open('contact_inquiries.txt', 'r') as file:
            for line in file:
                name, email, message = line.strip().split('|')
                inquiries.append(ContactInquiry(name, email, message))
    except FileNotFoundError:
        print("Contact inquiries file not found.")
    return inquiries

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('forum'))
        return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/forum')
def forum():
    threads = load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    threads = load_threads()
    comments = load_comments()
    if thread_id < len(threads):
        thread = threads[thread_id]
        if request.method == 'POST':
            content = request.form['content']
            new_comment = Comment(thread_id, content)
            new_comment.save()
            return redirect(url_for('view_thread', thread_id=thread_id))
        return render_template('view_thread.html', thread=thread, comments=comments)
    return redirect(url_for('forum'))

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_thread = Thread(title, content)
        new_thread.save()
        return redirect(url_for('forum'))
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
        new_inquiry = ContactInquiry(name, email, message)
        new_inquiry.save()
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8461, debug=False)
