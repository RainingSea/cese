from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from post import Post
from auth import Auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and posts from files
users = User.load_users()
posts = Post.load_posts()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        auth = Auth()
        if auth.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main')
def main():
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        post = Post(title, content, author)
        post.save()
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = posts[post_id]
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = posts[post_id]
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        post.edit(new_title, new_content)
        return redirect(url_for('main'))
    return render_template('edit_post.html', post=post)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8978, debug=False)
