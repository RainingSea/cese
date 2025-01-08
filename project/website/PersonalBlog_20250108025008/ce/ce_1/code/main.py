from flask import Flask, render_template, redirect, request, session
from auth import Auth
from blog import Blog

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a more secure secret key
auth = Auth()
blog = Blog()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.login(username, password):
            session['username'] = username
            return redirect('/main_blog')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth.register(username, password, email):
            return redirect('/')
        else:
            return "Registration failed"
    return render_template('registration.html')

@app.route('/main_blog')
def main_blog():
    posts = blog.list_posts()
    return render_template('main_blog.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog.create_post(title, content)
        return redirect('/main_blog')
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = blog.view_post(post_id)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog.edit_post(post_id, title, content)
        return redirect('/main_blog')
    post = blog.view_post(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8329, debug=False)
