from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import os
from user_manager import UserManager
from thread_manager import ThreadManager
from comment_manager import CommentManager
from advice_manager import AdviceManager
from contact_manager import ContactManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.thread_manager = ThreadManager()
        self.comment_manager = CommentManager()
        self.advice_manager = AdviceManager()
        self.contact_manager = ContactManager()

    @app.route('/', methods=['GET', 'POST'])
    def main():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if main.user_manager.login(username, password):
                session['username'] = username
                return redirect('/home')
            else:
                return render_template('login.html', error="Invalid credentials")
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if main.user_manager.register(username, password):
            return redirect('/')
        else:
            return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect('/')

@app.route('/forum')
def forum():
    threads = main.thread_manager.get_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    thread_details = main.thread_manager.get_thread_details(thread_id)
    comments = main.comment_manager.get_comments(thread_id)
    if request.method == 'POST':
        comment = request.form['comment']
        main.comment_manager.add_comment(thread_id, comment)
        return redirect(f'/view_thread/{thread_id}')
    return render_template('view_thread.html', thread=thread_details, comments=comments)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        main.advice_manager.post_advice(title, content)
        return redirect('/home')
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
        main.contact_manager.submit_inquiry(name, email, message)
        return redirect('/home')
    return render_template('contact_us.html')

if __name__ == '__main__':
    main = Main()
    app.run(port=8389, debug=False)
