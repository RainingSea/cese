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

@app.route('/main', methods=['GET'])
def main():
    if 'username' in session:
        posts = blog.get_posts_by_user(session['username'])
        return render_template('main.html', posts=posts)
    return redirect(url_for('login'))

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            blog.create_post(title, content, session['username'])
            return redirect(url_for('main'))
        return render_template('new_post.html')
    return redirect(url_for('login'))

@app.route('/view_post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = blog.load_posts()[post_id]
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'username' in session:
        post = blog.load_posts()[post_id]
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            blog.edit_post(title, content, post_id)
            return redirect(url_for('main'))
        return render_template('edit_post.html', post=post)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8480, debug=False)
