from flask import Flask, render_template, request, redirect, url_for, flash, session
from typing import List

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_users() -> List['User']:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
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
    def load_posts() -> List['Post']:
        posts = []
        try:
            with open('posts.txt', 'r') as f:
                for line in f:
                    title, content, author = line.strip().split('|')
                    posts.append(Post(title, content, author))
        except FileNotFoundError:
            pass
        return posts

class Auth:
    @staticmethod
    def login(username: str, password: str) -> bool:
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                flash("Login successful!", "success")
                return True
        flash("Invalid username or password!", "error")
        return False

    @staticmethod
    def register(username: str, password: str, email: str) -> bool:
        users = User.load_users()
        if any(user.username == username for user in users):
            flash("Username already exists!", "error")
            return False
        new_user = User(username, password, email)
        new_user.save()
        flash("Registration successful!", "success")
        return True

class Blog:
    @staticmethod
    def create_post(title: str, content: str, author: str):
        new_post = Post(title, content, author)
        new_post.save()
        flash("Post created successfully!", "success")

    @staticmethod
    def edit_post(title: str, content: str):
        posts = Post.load_posts()
        for post in posts:
            if post.title == title:
                post.content = content
                with open('posts.txt', 'w') as f:
                    for p in posts:
                        f.write(f"{p.title}|{p.content}|{p.author}\n")
                flash("Post edited successfully!", "success")
                return
        flash("Post not found!", "error")

    @staticmethod
    def delete_post(title: str):
        posts = Post.load_posts()
        posts = [post for post in posts if post.title != title]
        with open('posts.txt', 'w') as f:
            for post in posts:
                f.write(f"{post.title}|{post.content}|{post.author}\n")
        flash("Post deleted successfully!", "success")

    @staticmethod
    def view_post(title: str) -> str:
        posts = Post.load_posts()
        for post in posts:
            if post.title == title:
                return post.content
        return "Post not found!"

    @staticmethod
    def list_posts() -> List[Post]:
        return Post.load_posts()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        Auth.register(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main', methods=['GET'])
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = Blog.list_posts()
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        Blog.create_post(title, content, author)
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view_post/<title>', methods=['GET'])
def view_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    content = Blog.view_post(title)
    return render_template('view_post.html', title=title, content=content)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        content = request.form['content']
        Blog.edit_post(title, content)
        return redirect(url_for('main'))
    return render_template('edit_post.html', title=title)

@app.route('/delete_post/<title>', methods=['POST'])
def delete_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    Blog.delete_post(title)
    return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8140, debug=True)
