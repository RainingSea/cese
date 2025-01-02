from flask import Flask, render_template, request, redirect, url_for, session, flash
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Data structures
class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username},{self.password},{self.email}\n")

class BlogPost:
    def __init__(self, post_id: int, title: str, content: str):
        self.post_id = post_id
        self.title = title
        self.content = content

    def save(self):
        with open('posts.txt', 'a') as f:
            f.write(f"{self.post_id},{self.title},{self.content}\n")

    def delete(self):
        # This method will be implemented later
        pass

class BlogApp:
    def __init__(self):
        self.users: List[User] = []
        self.posts: List[BlogPost] = []
        self.load_users()
        self.load_posts()

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split(',')
                    self.users.append(User(username, password, email))

    def load_posts(self):
        if os.path.exists('posts.txt'):
            with open('posts.txt', 'r') as f:
                for line in f:
                    post_id, title, content = line.strip().split(',', 2)
                    self.posts.append(BlogPost(int(post_id), title, content))

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, email)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def create_post(self, title: str, content: str) -> None:
        post_id = len(self.posts) + 1
        new_post = BlogPost(post_id, title, content)
        new_post.save()
        self.posts.append(new_post)

    def edit_post(self, post_id: int, title: str, content: str) -> None:
        for post in self.posts:
            if post.post_id == post_id:
                post.title = title
                post.content = content
                self.save_posts()
                break

    def delete_post(self, post_id: int) -> None:
        self.posts = [post for post in self.posts if post.post_id != post_id]
        self.save_posts()

    def save_posts(self) -> None:
        with open('posts.txt', 'w') as f:
            for post in self.posts:
                f.write(f"{post.post_id},{post.title},{post.content}\n")

    def get_posts(self) -> List[BlogPost]:
        return self.posts

    def get_post(self, post_id: int) -> BlogPost:
        for post in self.posts:
            if post.post_id == post_id:
                return post
        return None

blog_app = BlogApp()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if blog_app.login(username, password):
        flash('Login successful! Welcome back.')
        return redirect(url_for('main'))
    else:
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if blog_app.register(username, password, email):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another one.')
    return render_template('register.html')

@app.route('/main', methods=['GET'])
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = blog_app.get_posts()
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_app.create_post(title, content)
        flash('Post created successfully!')
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view/<int:post_id>', methods=['GET'])
def view_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = blog_app.get_post(post_id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('main'))
    return render_template('view_post.html', post=post)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = blog_app.get_post(post_id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('main'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_app.edit_post(post_id, title, content)
        flash('Post updated successfully!')
        return redirect(url_for('view_post', post_id=post_id))
    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    blog_app.delete_post(post_id)
    flash('Post deleted successfully!')
    return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8180, debug=True)
