from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from blog_post import BlogPost
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = []
posts = []

def load_users():
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))

def load_posts():
    if os.path.exists('posts.txt'):
        with open('posts.txt', 'r') as f:
            for line in f:
                title, content, author = line.strip().split('|')
                posts.append(BlogPost(title, content, author))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        users.append(user)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        post = BlogPost(title, content, author)
        posts.append(post)
        post.save()
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = posts[post_id]
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = posts[post_id]
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.save()
        return redirect(url_for('main'))
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    posts.pop(post_id)
    return redirect(url_for('main'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('main'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    load_users()
    load_posts()
    app.run(port=8187, debug=False)
