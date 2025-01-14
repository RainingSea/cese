from flask import Flask, render_template, request, redirect, url_for, session
from Auth import Auth
from Blog import Blog

app = Flask(__name__)
app.secret_key = 'your_secret_key'
auth = Auth()
blog = Blog()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog.create_post(title, content)
    posts = blog.get_posts()
    return render_template('main.html', posts=posts)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if auth.login(username, password):
        session['username'] = username
        return redirect(url_for('main'))
    return redirect(url_for('login'))

@app.route('/new_post', methods=['GET'])
def new_post():
    return render_template('new_post.html')

@app.route('/view_post/<title>', methods=['GET'])
def view_post(title):
    posts = blog.get_posts()
    post = next((p for p in posts if p.title == title), None)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        blog.edit_post(title, new_title, new_content)
        return redirect(url_for('main'))
    posts = blog.get_posts()
    post = next((p for p in posts if p.title == title), None)
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<title>', methods=['POST'])
def delete_post(title):
    blog.delete_post(title)
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(port=8462, debug=False)
