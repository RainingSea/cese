from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from blog_post import BlogPost
from file_manager import FileManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

file_manager = FileManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        if user.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = file_manager.load_posts()
    return render_template('main.html', posts=posts)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('main'))
    return redirect(url_for('login'))

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
        author = session['username']
        post = BlogPost(title, content, author)
        file_manager.save_post(post)
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view/<title>', methods=['GET'])
def view_post(title):
    posts = file_manager.load_posts()
    for post in posts:
        if post[0] == title:
            return render_template('view_post.html', post=BlogPost(post[0], post[1], post[2]))
    return redirect(url_for('main'))

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = file_manager.load_posts()
    for post in posts:
        if post[0] == title:
            if request.method == 'POST':
                content = request.form['content']
                post_obj = BlogPost(title, content, session['username'])
                post_obj.edit_post(title, content)
                return redirect(url_for('main'))
            return render_template('edit_post.html', post=BlogPost(post[0], post[1], post[2]))
    return redirect(url_for('main'))

@app.route('/delete_post/<title>', methods=['POST'])
def delete_post(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = BlogPost(title, '', '')
    post.delete_post()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(port=8074, debug=False)
