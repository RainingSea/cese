from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_users():
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

class Post:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")

    @staticmethod
    def load_posts():
        posts = []
        if os.path.exists('posts.txt'):
            with open('posts.txt', 'r') as f:
                for line in f:
                    title, content, author = line.strip().split('|')
                    posts.append(Post(title, content, author))
        return posts

class Auth:
    @staticmethod
    def login(username: str, password: str) -> bool:
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    @staticmethod
    def register(username: str, password: str, email: str) -> bool:
        users = User.load_users()
        if any(user.username == username for user in users):
            return False
        new_user = User(username, password, email)
        new_user.save()
        return True

class Blog:
    @staticmethod
    def create_post(title: str, content: str, author: str):
        new_post = Post(title, content, author)
        new_post.save()

    @staticmethod
    def edit_post(title: str, content: str):
        posts = Post.load_posts()
        for post in posts:
            if post.title == title:
                post.content = content
                break
        with open('posts.txt', 'w') as f:
            for post in posts:
                f.write(f"{post.title}|{post.content}|{post.author}\n")

    @staticmethod
    def delete_post(title: str):
        posts = Post.load_posts()
        posts = [post for post in posts if post.title != title]
        with open('posts.txt', 'w') as f:
            for post in posts:
                f.write(f"{post.title}|{post.content}|{post.author}\n")

    @staticmethod
    def view_post(title: str) -> str:
        posts = Post.load_posts()
        for post in posts:
            if post.title == title:
                return post.content
        return ""

    @staticmethod
    def list_posts() -> list:
        return Post.load_posts()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if Auth.login(username, password):
        flash("Login successful!", "success")
        return redirect(url_for('main'))
    else:
        flash("Login failed. Please check your username and password.", "error")
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if Auth.register(username, password, email):
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('login'))
        else:
            flash("Registration failed. Username may already exist.", "error")
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        Blog.create_post(title, content, author)
        flash("Post created successfully!", "success")
        return redirect(url_for('main'))
    posts = Blog.list_posts()
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        Blog.create_post(title, content, author)
        flash("Post created successfully!", "success")
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view_post/<title>')
def view_post(title):
    content = Blog.view_post(title)
    return render_template('view_post.html', title=title, content=content)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if request.method == 'POST':
        content = request.form['content']
        Blog.edit_post(title, content)
        flash("Post updated successfully!", "success")
        return redirect(url_for('main'))
    return render_template('edit_post.html', title=title)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8139, debug=True)
