from flask import Flask, render_template, request, redirect, session
from user import User
from thread import Thread
from comment import Comment
from contact_inquiry import ContactInquiry

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_threads():
    threads = []
    with open('threads.txt', 'r') as file:
        for line in file:
            title, content = line.strip().split('|')
            threads.append(Thread(title, content))
    return threads

def load_comments():
    comments = []
    with open('comments.txt', 'r') as file:
        for line in file:
            content = line.strip()
            comments.append(Comment(content))
    return comments

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
        return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    threads = load_threads()
    return render_template('home.html', threads=threads)

@app.route('/forum')
def forum():
    threads = load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>')
def view_thread(thread_id):
    threads = load_threads()
    thread = threads[thread_id]
    comments = load_comments()
    return render_template('view_thread.html', thread=thread, comments=comments)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread = Thread(title, content)
        thread.save()
        return redirect('/forum')
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
        inquiry = ContactInquiry(name, email, message)
        inquiry.save()
        return redirect('/contact_us')
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8563, debug=False)
