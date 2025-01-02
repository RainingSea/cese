from flask import Flask, render_template, request, redirect, url_for, flash
from user import User
from thread import Thread
from comment import Comment
from advice import Advice  # Import Advice class

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Load users from the text file
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')[:2]
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

# Load threads from the text file
def load_threads():
    threads = []
    try:
        with open('threads.txt', 'r') as file:
            for line in file:
                title, content, author = line.strip().split('|')[:3]
                threads.append(Thread(title, content, author))
    except FileNotFoundError:
        pass
    return threads

# Load comments from the text file
def load_comments():
    comments = []
    try:
        with open('comments.txt', 'r') as file:
            for line in file:
                thread_id, content, author = line.strip().split('|')[:3]
                comments.append(Comment(int(thread_id), content, author))
    except FileNotFoundError:
        pass
    return comments

# Load advice from the text file
def load_advice():
    advice_list = []
    try:
        with open('advice.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')[:2]
                advice_list.append(Advice(title, content))
    except FileNotFoundError:
        pass
    return advice_list

users = load_users()
threads = load_threads()
comments = load_comments()
advice_list = load_advice()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            new_user = User(username, password)
            new_user.save()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Please fill in all fields.', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user.username == username and user.password == password:
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']  # Assuming author is passed from the session or form
        if title and content:
            new_thread = Thread(title, content, author)
            new_thread.save()
            flash('Thread created successfully!', 'success')
            return redirect(url_for('forum'))
        else:
            flash('Please fill in all fields.', 'danger')
    return render_template('forum.html', threads=threads)

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    if request.method == 'POST':
        content = request.form['content']
        author = request.form['author']  # Assuming author is passed from the session or form
        if content:
            new_comment = Comment(thread_id, content, author)
            new_comment.save()
            flash('Comment added successfully!', 'success')
            return redirect(url_for('view_thread', thread_id=thread_id))
        else:
            flash('Please fill in all fields.', 'danger')
    
    # Find the thread by ID
    thread = next((t for t in threads if threads.index(t) == thread_id), None)
    thread_comments = [c for c in comments if c.thread_id == thread_id]
    
    return render_template('view_thread.html', thread=thread, comments=thread_comments)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title and content:
            new_advice = Advice(title, content)
            new_advice.save()
            flash('Advice posted successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please fill in all fields.', 'danger')
    return render_template('post_advice.html')

if __name__ == '__main__':
    app.run(port=8168, debug=True)
