from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def update_profile(self, username: str, new_info: dict) -> bool:
        for user in self.users:
            if user['username'] == username:
                user.update(new_info)
                self.save_users()
                return True
        return False

    def delete_account(self, username: str) -> bool:
        self.users = [user for user in self.users if user['username'] != username]
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write(f"{user['username']}|{user['password']}\n")

class ThreadManager:
    def __init__(self):
        self.threads = self.load_threads()

    def load_threads(self):
        threads = []
        if os.path.exists('threads.txt'):
            with open('threads.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    threads.append({'title': title, 'content': content})
        return threads

    def create_thread(self, title: str, content: str) -> bool:
        self.threads.append({'title': title, 'content': content})
        with open('threads.txt', 'a') as f:
            f.write(f"{title}|{content}\n")
        return True

    def get_threads(self):
        return self.threads

    def get_thread_details(self, thread_id: int) -> dict:
        return self.threads[thread_id] if 0 <= thread_id < len(self.threads) else {}

class CommentManager:
    def __init__(self):
        self.comments = self.load_comments()

    def load_comments(self):
        comments = []
        if os.path.exists('comments.txt'):
            with open('comments.txt', 'r') as f:
                for line in f:
                    thread_id, comment = line.strip().split('|')
                    comments.append({'thread_id': int(thread_id), 'comment': comment})
        return comments

    def add_comment(self, thread_id: int, comment: str) -> bool:
        self.comments.append({'thread_id': thread_id, 'comment': comment})
        with open('comments.txt', 'a') as f:
            f.write(f"{thread_id}|{comment}\n")
        return True

    def get_comments(self, thread_id: int) -> list:
        return [comment for comment in self.comments if comment['thread_id'] == thread_id]

class AdviceManager:
    def __init__(self):
        self.advice_posts = self.load_advice()

    def load_advice(self):
        advice_posts = []
        if os.path.exists('advice.txt'):
            with open('advice.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    advice_posts.append({'title': title, 'content': content})
        return advice_posts

    def post_advice(self, title: str, content: str) -> bool:
        self.advice_posts.append({'title': title, 'content': content})
        with open('advice.txt', 'a') as f:
            f.write(f"{title}|{content}\n")
        return True

    def get_advice(self):
        return self.advice_posts

user_manager = UserManager()
thread_manager = ThreadManager()
comment_manager = CommentManager()
advice_manager = AdviceManager()

@login_manager.user_loader
def load_user(user_id):
    return UserMixin()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/forum')
@login_required
def forum():
    threads = thread_manager.get_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>')
@login_required
def view_thread(thread_id):
    thread_details = thread_manager.get_thread_details(thread_id)
    comments = comment_manager.get_comments(thread_id)
    return render_template('view_thread.html', thread=thread_details, comments=comments)

@app.route('/post_advice', methods=['GET', 'POST'])
@login_required
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        advice_manager.post_advice(title, content)
        return redirect(url_for('home'))
    return render_template('post_advice.html')

@app.route('/my_account')
@login_required
def my_account():
    return render_template('my_account.html')

@app.route('/contact_us')
@login_required
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8386, debug=False)
