from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from thread import Thread
from comment import Comment
from advice import Advice
from contact_inquiry import ContactInquiry

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

def load_users() -> list:
    """Load users from the users.txt file."""
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass  # Handle the case where the file does not exist
    return users

def load_threads() -> list:
    """Load threads from the threads.txt file."""
    threads = []
    try:
        with open('threads.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                threads.append(Thread(title, content))
    except FileNotFoundError:
        pass  # Handle the case where the file does not exist
    return threads

@app.route('/')
def login() -> str:
    """Render the login page."""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate() -> str:
    """Authenticate user login."""
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register() -> str:
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home() -> str:
    """Render the home page after login."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/forum')
def forum() -> str:
    """Render the forum page with threads."""
    if 'username' not in session:
        return redirect(url_for('login'))
    threads = load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id: int) -> str:
    """Render a specific thread and handle comments."""
    if 'username' not in session:
        return redirect(url_for('login'))
    threads = load_threads()
    if thread_id < len(threads):
        thread = threads[thread_id]
        if request.method == 'POST':
            comment_content = request.form['comment']
            thread.add_comment(comment_content)
            return redirect(url_for('view_thread', thread_id=thread_id))
        return render_template('view_thread.html', thread=thread)
    return redirect(url_for('forum'))

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice() -> str:
    """Handle posting advice."""
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
def my_account() -> str:
    """Render the user's account page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('my_account.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us() -> str:
    """Handle contact inquiries."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        inquiry = ContactInquiry(name, email, message)
        inquiry.save()
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8476, debug=False)
