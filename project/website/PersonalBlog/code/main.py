from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = (password, email)
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        self.users[username] = (password, email)
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username][0] == password:
            return True
        return False

class BlogPost:
    def __init__(self, post_id, username, title, content, timestamp):
        self.post_id = post_id
        self.username = username
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def create_post(self, username: str, title: str, content: str) -> bool:
        post_id = self.get_next_post_id()
        timestamp = self.get_current_timestamp()
        with open('posts.txt', 'a') as f:
            f.write(f"{post_id}|{username}|{title}|{content}|{timestamp}\n")
        return True

    def edit_post(self, post_id: int, title: str, content: str) -> bool:
        posts = self.load_posts()
        for post in posts:
            if post.post_id == post_id:
                post.title = title
                post.content = content
                self.save_posts(posts)
                return True
        return False

    def delete_post(self, post_id: int) -> bool:
        posts = self.load_posts()
        posts = [post for post in posts if post.post_id != post_id]
        self.save_posts(posts)
        return True

    def view_post(self, post_id: int) -> str:
        posts = self.load_posts()
        for post in posts:
            if post.post_id == post_id:
                return post.content
        return ""

    def get_next_post_id(self) -> int:
        posts = self.load_posts()
        return len(posts) + 1

    def get_current_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def load_posts(self):
        posts = []
        if os.path.exists('posts.txt'):
            with open('posts.txt', 'r') as f:
                for line in f:
                    post_data = line.strip().split('|')
                    post = BlogPost(int(post_data[0]), post_data[1], post_data[2], post_data[3], post_data[4])
                    posts.append(post)
        return posts

    def save_posts(self, posts):
        with open('posts.txt', 'w') as f:
            for post in posts:
                f.write(f"{post.post_id}|{post.username}|{post.title}|{post.content}|{post.timestamp}\n")

user_manager = UserManager('users.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('main_blog'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/main_blog')
def main_blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    blog_manager = BlogPost(0, "", "", "", "")
    posts = blog_manager.load_posts()
    return render_template('main_blog.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_post = BlogPost(0, session['username'], title, content, "")
        blog_post.create_post(session['username'], title, content)
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    blog_post = BlogPost(0, "", "", "", "")
    content = blog_post.view_post(post_id)
    return render_template('view_post.html', content=content)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    blog_post = BlogPost(0, "", "", "", "")
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if blog_post.edit_post(post_id, title, content):
            return redirect(url_for('main_blog'))
    return render_template('edit_post.html', post_id=post_id)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    blog_post = BlogPost(0, "", "", "", "")
    blog_post.delete_post(post_id)
    return redirect(url_for('main_blog'))

if __name__ == '__main__':
    app.run(port=8397, debug=False)
