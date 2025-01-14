from flask import Flask, render_template, request, redirect, url_for, session, flash
from user import User
from thread import Thread
from comment import Comment
from contact import Contact

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')[:2]
                users.append(User(username, password))
    except FileNotFoundError:
        flash('User data file not found.')
    return users

def load_threads():
    threads = []
    try:
        with open('threads.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')[:2]
                threads.append(Thread(title, content))
    except FileNotFoundError:
        flash('Thread data file not found.')
    return threads

def load_comments():
    comments = []
    try:
        with open('comments.txt', 'r') as file:
            for line in file:
                content = line.strip()
                comments.append(Comment(content))
    except FileNotFoundError:
        flash('Comment data file not found.')
    return comments

def load_contacts():
    contacts = []
    try:
        with open('contacts.txt', 'r') as file:
            for line in file:
                name, email, message = line.strip().split('|')
                contacts.append(Contact(name, email, message))
    except FileNotFoundError:
        flash('Contact data file not found.')
    return contacts

@app.route('/')
def login():
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
    if thread_id < len(threads):
        thread = threads[thread_id]
        comments = load_comments()
        return render_template('view_thread.html', thread=thread, comments=comments)
    else:
        flash('Thread not found.')
        return redirect(url_for('forum'))

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_thread = Thread(title, content)
        new_thread.save()
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
        new_contact = Contact(name, email, message)
        new_contact.save()
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8073, debug=False)
