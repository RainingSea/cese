from flask import Flask, render_template, request, redirect, url_for, session
from auth import Auth
from blog import Blog

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
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
        else:
            return "Username already exists!"
    return render_template('registration.html')


@app.route('/main_blog', methods=['GET'])
def main_blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = blog.list_posts()
    return render_template('main_blog.html', posts=posts)


@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog.create_post(title, content)
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')


@app.route('/view_post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = blog.view_post(post_id)
    return render_template('view_post.html', post=post)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = blog.view_post(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog.edit_post(post_id, title, content)
        return redirect(url_for('main_blog'))
    return render_template('edit_post.html', post=post)


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if auth.login(username, password):
        session['username'] = username
        return redirect(url_for('main_blog'))
    return "Invalid credentials!"


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=8330, debug=False)
