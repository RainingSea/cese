from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from PostManager import PostManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    return render_template('register.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        content = request.form['content']
        post_manager.create_post(username, title, content)
    posts = post_manager.load_posts()
    return render_template('main.html', posts=posts)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('main'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/new_post')
def new_post():
    return render_template('new_post.html')

@app.route('/view_post/<title>')
def view_post(title):
    post = post_manager.get_post(title)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if request.method == 'POST':
        new_title = request.form['new_title']
        new_content = request.form['new_content']
        post_manager.delete_post(title)
        post_manager.create_post(session['username'], new_title, new_content)
        return redirect(url_for('main'))
    post = post_manager.get_post(title)
    return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    app.run(port=8479, debug=False)
