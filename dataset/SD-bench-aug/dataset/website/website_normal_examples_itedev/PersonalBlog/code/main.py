from flask import Flask, render_template, request, redirect, url_for, session, flash
from UserManager import UserManager
from PostManager import PostManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # This should be securely managed in production

# Initialize UserManager and PostManager
user_manager = UserManager('users.txt')
post_manager = PostManager('posts.txt')

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('main_blog'))
    else:
        flash('Login failed. Please check your username and password.')
        return redirect(url_for('login'))

@app.route('/main_blog')
def main_blog():
    """Render the main blog page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = post_manager.get_posts(session['username'])
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    """Handle creating a new blog post."""
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post_manager.create_post(title, content, session['username'])
        flash('Post created successfully!')
        return redirect(url_for('main_blog'))
    return render_template('new_post.html')

@app.route('/view_post/<title>')
def view_post(title):
    """Render a specific blog post."""
    if 'username' not in session:
        return redirect(url_for('login'))
    post = post_manager.get_post(title, session['username'])
    if not post:
        flash('Post not found.')
        return redirect(url_for('main_blog'))
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    """Handle editing an existing blog post."""
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        if post_manager.edit_post(title, new_title, new_content, session['username']):
            flash('Post updated successfully!')
            return redirect(url_for('main_blog'))
        else:
            flash('Error updating post.')
    post = post_manager.get_post(title, session['username'])
    if not post:
        flash('Post not found.')
        return redirect(url_for('main_blog'))
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<title>', methods=['POST'])
def delete_post(title):
    """Handle deleting a blog post."""
    if 'username' not in session:
        return redirect(url_for('login'))
    if post_manager.delete_post(title, session['username']):
        flash('Post deleted successfully!')
    else:
        flash('Error deleting post.')
    return redirect(url_for('main_blog'))

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5002,debug=True)