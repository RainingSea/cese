from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from post import Post
from auth import Auth
from blog import Blog

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth = Auth()
blog = Blog()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        blog.create_post(title, content, author)
    posts = blog.load_posts()
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        blog.create_post(title, content, author)
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view_post/<title>', methods=['GET'])
def view_post(title):
    post_content = blog.view_post(title)
    return render_template('view_post.html', title=title, content=post_content)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if request.method == 'POST':
        content = request.form['content']
        blog.edit_post(title, content)
        return redirect(url_for('main'))
    post_content = blog.view_post(title)
    return render_template('edit_post.html', title=title, content=post_content)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8977, debug=False)
