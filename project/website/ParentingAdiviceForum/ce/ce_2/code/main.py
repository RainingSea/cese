from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('threads.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

class Comment:
    def __init__(self, thread_id: int, content: str):
        self.thread_id = thread_id
        self.content = content

    def save(self):
        with open('comments.txt', 'a') as f:
            f.write(f"{self.thread_id}|{self.content}\n")

class ContactInquiry:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def save(self):
        with open('contact_inquiries.txt', 'a') as f:
            f.write(f"{self.name}|{self.email}|{self.message}\n")

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
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = []
    if os.path.exists('threads.txt'):
        with open('threads.txt', 'r') as f:
            threads = f.readlines()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>')
def view_thread(thread_id):
    thread_details = ""
    if os.path.exists('threads.txt'):
        with open('threads.txt', 'r') as f:
            threads = f.readlines()
            if thread_id < len(threads):
                thread_details = threads[thread_id]
    return render_template('view_thread.html', thread_details=thread_details)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread = Thread(title, content)
        thread.save()
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
        inquiry = ContactInquiry(name, email, message)
        inquiry.save()
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8564, debug=False)
