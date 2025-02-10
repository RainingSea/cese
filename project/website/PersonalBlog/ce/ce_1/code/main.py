from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from blog_post import BlogPost
from blog_manager import BlogManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
blog_manager = BlogManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if blog_manager.register_user(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main_blog', methods=['GET', 'POST'])
def main_blog():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        content = request.form['content']
        blog_manager.create_post(title, content, username)
    posts = blog_manager.view_posts(session['username'])
    return render_template('main_blog.html', posts=posts)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if blog_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('main_blog'))
    return redirect(url_for('login'))

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = blog_manager.get_post(post_id)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_manager.edit_post(post_id, title, content)
        return redirect(url_for('main_blog'))
    post = blog_manager.get_post(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    blog_manager.delete_post(post_id)
    return redirect(url_for('main_blog'))

if __name__ == '__main__':
    app.run(port=8569, debug=False)
