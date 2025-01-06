from flask import Flask, render_template, request, redirect, session
from user import User
from blog_post import BlogPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = []
posts = []

def load_users():
    global users
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    except FileNotFoundError:
        pass

def load_posts():
    global posts
    try:
        with open('posts.txt', 'r') as file:
            for line in file:
                title, content, author = line.strip().split('|')
                posts.append(BlogPost(title, content, author))
    except FileNotFoundError:
        pass

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        users.append(new_user)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return redirect('/')

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
        new_post = BlogPost(title, content, author)
        posts.append(new_post)
        with open('posts.txt', 'a') as file:
            file.write(f"{title}|{content}|{author}\n")
        return redirect('/main')

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
        return redirect('/main')

    return render_template('edit_post.html', post=post)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    load_users()
    load_posts()
    app.run(port=8189, debug=False)
