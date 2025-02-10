from flask import Flask, render_template, request, redirect, session, url_for
from UserManager import UserManager
from PostManager import PostManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
post_manager = PostManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('main_blog'))
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

@app.route('/main_blog')
def main_blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = post_manager.load_posts(session['username'])
    return render_template('main_blog.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post_manager.create_post(session['username'], title, content)
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')

@app.route('/view_post/<title>')
def view_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = post_manager.load_all_posts()
    post = next((p for p in posts if p.title == title), None)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        content = request.form['content']
        post_manager.edit_post(title, content)
        return redirect(url_for('main_blog'))
    posts = post_manager.load_all_posts()
    post = next((p for p in posts if p.title == title), None)
    return render_template('edit_post.html', post=post)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8572, debug=False)
