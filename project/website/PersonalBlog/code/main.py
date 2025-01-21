from flask import Flask, render_template, request, redirect, url_for, session
from user import User, UserManager
from post import Post, PostManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
post_manager = PostManager('posts.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('main_blog'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/main_blog')
def main_blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = post_manager.load_posts()
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session['username']
        post_manager.create_post(username, title, content)
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')

@app.route('/view_post/<title>')
def view_post(title):
    post = post_manager.get_post(title)
    if post is None:
        return redirect(url_for('main_blog'))  # Redirect if post not found
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = post_manager.get_post(title)
    if post is None:
        return redirect(url_for('main_blog'))  # Redirect if post not found
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        post_manager.edit_post(title, new_title, new_content)
        return redirect(url_for('main_blog'))
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<title>', methods=['POST'])
def delete_post(title):
    post_manager.delete_post(title)
    return redirect(url_for('main_blog'))

if __name__ == '__main__':
    app.run(port=8979, debug=False)
