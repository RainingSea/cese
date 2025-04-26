from flask import Flask, request, render_template, redirect, url_for, flash, session
from user_manager import UserManager
from post_manager import PostManager

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
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.')
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username  # Store username in session
        return redirect(url_for('main_blog'))
    else:
        flash('Login failed. Check your username and password.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/main_blog')
def main_blog():
    posts = post_manager.get_posts()
    return render_template('main_blog.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session.get('username')  # Get username from session
        if post_manager.create_post(title, content, username):
            flash('Post created successfully!')
            return redirect(url_for('main_blog'))
        else:
            flash('Failed to create post.')
    return render_template('new_post.html', username=session.get('username'))

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = post_manager.get_post(post_id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('main_blog'))
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = post_manager.get_post(post_id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('main_blog'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if post_manager.edit_post(post_id, title, content):
            flash('Post updated successfully!')
            return redirect(url_for('main_blog'))
        else:
            flash('Failed to update post.')
    
    return render_template('edit_post.html', post=post, post_id=post_id)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if post_manager.delete_post(post_id):
        flash('Post deleted successfully!')
    else:
        flash('Failed to delete post.')
    return redirect(url_for('main_blog'))

if __name__ == '__main__':
    app.run(port=8225, debug=False)
