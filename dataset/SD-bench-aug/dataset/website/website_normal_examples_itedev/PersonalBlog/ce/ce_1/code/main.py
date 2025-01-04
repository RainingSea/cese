from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from PostManager import PostManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

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
        else:
            return "Registration failed. Username may already exist."
    return render_template('register.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    posts = post_manager.get_posts(username)
    return render_template('main.html', posts=posts)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('main'))
    return "Login failed. Please check your username and password."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session['username']
        post_manager.create_post(title, content, username)
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view/<title>', methods=['GET'])
def view_post(title):
    post = post_manager.get_post(title)
    if not post:
        return "Post not found."
    return render_template('view_post.html', post=post)

@app.route('/edit/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = post_manager.get_post(title)
    if request.method == 'POST':
        new_title = request.form['new_title']
        new_content = request.form['new_content']
        post_manager.edit_post(title, new_title, new_content)
        return redirect(url_for('main'))
    return render_template('edit_post.html', post=post)

@app.route('/delete/<title>', methods=['POST'])
def delete_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    post_manager.delete_post(title)
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)