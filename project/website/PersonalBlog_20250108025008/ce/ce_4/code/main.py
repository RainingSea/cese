from flask import Flask, render_template, request, redirect, url_for, session
from auth import Auth
from blog import Blog

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production
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
    return render_template('registration.html')

@app.route('/main', methods=['GET', 'POST'])
def main_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog.create_post(title, content)
        return redirect(url_for('main_blog'))
    posts = blog.list_posts()
    return render_template('main_blog.html', posts=posts)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if auth.login(username, password):
        session['username'] = username
        return redirect(url_for('main_blog'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = blog.view_post(post_id)
    return render_template('view_post.html', post=post)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = blog.view_post(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog.edit_post(post_id, title, content)
        return redirect(url_for('main_blog'))
    return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    app.run(port=8332, debug=False)
