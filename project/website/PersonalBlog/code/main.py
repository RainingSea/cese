from flask import Flask, render_template, request, redirect, url_for, flash
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
    def load_users() -> list:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

class Post:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self.username}|{self.title}|{self.content}\n")

    @staticmethod
    def load_posts() -> list:
        posts = []
        if os.path.exists('posts.txt'):
            with open('posts.txt', 'r') as f:
                for line in f:
                    username, title, content = line.strip().split('|')
                    posts.append(Post(username, title, content))
        return posts

    @staticmethod
    def delete_post(title: str) -> None:
        posts = Post.load_posts()
        with open('posts.txt', 'w') as f:
            for post in posts:
                if post.title != title:
                    f.write(f"{post.username}|{post.title}|{post.content}\n")

class Auth:
    @staticmethod
    def login(username: str, password: str) -> bool:
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
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

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Auth.login(username, password):
            flash('Login successful!', 'success')
            return redirect(url_for('main_blog'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if Auth.register(username, password, email):
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another one.', 'danger')
    return render_template('register.html')

@app.route('/main_blog')
def main_blog():
    posts = Post.load_posts()
    return render_template('main_blog.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        username = request.form['username']  # Assuming username is passed from session
        title = request.form['title']
        content = request.form['content']
        new_post = Post(username, title, content)
        new_post.save()
        flash('Post created successfully!', 'success')
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')

@app.route('/view_post/<title>')
def view_post(title):
    posts = Post.load_posts()
    post = next((p for p in posts if p.title == title), None)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    posts = Post.load_posts()
    post = next((p for p in posts if p.title == title), None)
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        Post.delete_post(title)
        updated_post = Post(post.username, new_title, new_content)
        updated_post.save()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('main_blog'))
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<title>', methods=['POST'])
def delete_post(title):
    Post.delete_post(title)
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('main_blog'))

if __name__ == '__main__':
    app.run(debug=True)