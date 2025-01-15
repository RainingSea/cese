from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from blog_manager import BlogManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
blog_manager = BlogManager('users.txt', 'posts.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if blog_manager.login_user(username, password):
        session['username'] = username
        return redirect(url_for('main'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if blog_manager.register_user(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main', methods=['GET'])
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = blog_manager.get_posts()
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        blog_manager.create_post(title, content, author)
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view_post/<title>', methods=['GET'])
def view_post(title):
    post = blog_manager.get_post(title)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        blog_manager.edit_post(title, new_title, new_content)
        return redirect(url_for('main'))
    post = blog_manager.get_post(title)
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<title>', methods=['POST'])
def delete_post(title):
    blog_manager.delete_post(title)
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(port=8548, debug=False)
