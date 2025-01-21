from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from post_manager import PostManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager()
post_manager = PostManager()

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
    return render_template('registration.html')

@app.route('/main_blog')
def main_blog():
    posts = post_manager.load_posts()
    return render_template('main_blog.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        post_manager.create_post(title, content, author)
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = post_manager.load_posts()[post_id]
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = post_manager.load_posts()[post_id]
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post_manager.edit_post(post_id, title, content)
        return redirect(url_for('main_blog'))
    return render_template('edit_post.html', post=post)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('main_blog'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8974, debug=False)
