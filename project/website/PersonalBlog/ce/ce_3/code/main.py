from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from post import Post
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users_file = 'users.txt'
posts_file = 'posts.txt'

class BlogApp:
    def __init__(self, users_file: str, posts_file: str):
        self.users_file = users_file
        self.posts_file = posts_file

    def load_users(self):
        users = []
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

    def load_posts(self):
        posts = []
        if os.path.exists(self.posts_file):
            with open(self.posts_file, 'r') as f:
                for line in f:
                    title, content, author = line.strip().split('|')
                    posts.append(Post(title, content, author))
        return posts

    def register_user(self, username: str, password: str, email: str) -> bool:
        users = self.load_users()
        for user in users:
            if user.username == username:
                return False
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True

    def login_user(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def create_post(self, title: str, content: str, author: str) -> None:
        with open(self.posts_file, 'a') as f:
            f.write(f"{title}|{content}|{author}\n")

    def get_posts(self) -> list:
        return self.load_posts()

    def get_post(self, title: str) -> Post:
        posts = self.load_posts()
        for post in posts:
            if post.title == title:
                return post
        return None

    def edit_post(self, title: str, new_title: str, new_content: str) -> None:
        posts = self.load_posts()
        with open(self.posts_file, 'w') as f:
            for post in posts:
                if post.title == title:
                    f.write(f"{new_title}|{new_content}|{post.author}\n")
                else:
                    f.write(post.to_string() + '\n')

    def delete_post(self, title: str) -> None:
        posts = self.load_posts()
        with open(self.posts_file, 'w') as f:
            for post in posts:
                if post.title != title:
                    f.write(post.to_string() + '\n')

blog_app = BlogApp(users_file, posts_file)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if blog_app.register_user(username, password, email):
            return redirect(url_for('login'))
        else:
            return "User already exists!"
    return render_template('register.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        blog_app.create_post(title, content, author)
        return redirect(url_for('main'))
    posts = blog_app.get_posts()
    return render_template('main.html', posts=posts)

@app.route('/view_post/<title>')
def view_post(title):
    post = blog_app.get_post(title)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    post = blog_app.get_post(title)
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        blog_app.edit_post(title, new_title, new_content)
        return redirect(url_for('main'))
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<title>', methods=['POST'])
def delete_post(title):
    blog_app.delete_post(title)
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(port=8571, debug=False)
