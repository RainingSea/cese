from flask import Flask, render_template, request, redirect, url_for, flash
from user import User
from blog_post import BlogPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and posts from files
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split('|')
            users[username] = User(username, password, email)
    return users

def load_posts():
    posts = {}
    with open('posts.txt', 'r') as file:
        for line in file:
            title, content, author = line.strip().split('|')
            posts[title] = BlogPost(title, content, author)
    return posts

users = load_users()
posts = load_posts()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username in users:
            flash('Username already exists.')
        else:
            users[username] = User(username, password, email)
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}|{email}\n")
            flash('Registration successful. Please log in.')
            return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/main', methods=['GET'])
def main_page():
    return render_template('main.html', posts=posts.values())

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        posts[title] = BlogPost(title, content, author)
        with open('posts.txt', 'a') as file:
            file.write(f"{title}|{content}|{author}\n")
        flash('Post created successfully.')
        return redirect(url_for('main_page'))
    return render_template('new_post.html')

@app.route('/view_post/<title>', methods=['GET'])
def view_post(title):
    post = posts.get(title)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    post = posts.get(title)
    if request.method == 'POST':
        post.content = request.form['content']
        with open('posts.txt', 'w') as file:
            for p in posts.values():
                file.write(f"{p.title}|{p.content}|{p.author}\n")
        flash('Post updated successfully.')
        return redirect(url_for('view_post', title=post.title))
    return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    app.run(port=8107, debug=False)
