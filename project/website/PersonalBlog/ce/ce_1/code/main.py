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
    return render_template('main.html', posts=blog.get_posts(session.get('username')))

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog.create_post(session.get('username'), title, content)
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = blog.get_post(post_id)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog.edit_post(post_id, title, content)
        return redirect(url_for('view_post', post_id=post_id))
    post = blog.get_post(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8975, debug=False)
