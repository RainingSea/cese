from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from blog_post import BlogPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and posts from files
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    except FileNotFoundError:
        pass
    return users

def load_posts():
    posts = []
    try:
        with open('posts.txt', 'r') as f:
            for line in f:
                title, content, author = line.strip().split('|')
                posts.append(BlogPost(title, content, author))
    except FileNotFoundError:
        pass
    return posts

users = load_users()
posts = load_posts()

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
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', posts=posts)

@app.route('/login', methods=['POST'])
def user_login():
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

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        post = BlogPost(title, content, author)
        posts.append(post)
        with open('posts.txt', 'a') as f:
            f.write(f"{title}|{content}|{author}\n")
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
        # Update the posts file
        with open('posts.txt', 'w') as f:
            for p in posts:
                f.write(f"{p.title}|{p.content}|{p.author}\n")
        return redirect(url_for('view_post', post_id=post_id))
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    del posts[post_id]
    # Update the posts file
    with open('posts.txt', 'w') as f:
        for p in posts:
            f.write(f"{p.title}|{p.content}|{p.author}\n")
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(port=8186, debug=False)
