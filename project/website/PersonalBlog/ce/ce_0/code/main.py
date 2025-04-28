from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from blog_manager import BlogManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
blog_manager = BlogManager('posts.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_manager.register(username, password, email)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/main_blog', methods=['GET'])
def main_blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = blog_manager.get_posts(session['username'])
    return render_template('main_blog.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_manager.create_post(session['username'], title, content)
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = blog_manager.get_posts(session['username'])[post_id]
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_manager.edit_post(post_id, title, content)
        return redirect(url_for('main_blog'))
    post = blog_manager.get_posts(session['username'])[post_id]
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    blog_manager.delete_post(post_id)
    return redirect(url_for('main_blog'))

if __name__ == '__main__':
    app.run(port=8394, debug=False)
