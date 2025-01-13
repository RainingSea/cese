from flask import Flask, render_template, request, redirect, session
from user import User
from post import Post

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

class BlogApp:
    def __init__(self):
        self.users = self.load_users()
        self.posts = self.load_posts()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users

    def load_posts(self):
        posts = []
        with open('posts.txt', 'r') as file:
            for line in file:
                username, title, content = line.strip().split('|')
                posts.append(Post(username, title, content))
        return posts

    def register(self, username, password, email):
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, email)
        self.users.append(new_user)
        new_user.save()
        return True

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def create_post(self, username, title, content):
        new_post = Post(username, title, content)
        self.posts.append(new_post)
        new_post.save()

    def get_posts(self, username):
        return [post for post in self.posts if post.username == username]

    def edit_post(self, username, title, new_content):
        for post in self.posts:
            if post.username == username and post.title == title:
                post.content = new_content
                post.save()
                break

    def delete_post(self, title):
        self.posts = [post for post in self.posts if post.title != title]
        self.save_posts()

    def save_posts(self):
        with open('posts.txt', 'w') as file:
            for post in self.posts:
                file.write(f"{post.username}|{post.title}|{post.content}\n")

blog_app = BlogApp()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if blog_app.register(username, password, email):
            return redirect('/')
        return "Registration failed. Username may already exist."
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if blog_app.login(username, password):
        return redirect('/main')
    return "Login failed. Check your credentials."

@app.route('/main')
def main_page():
    return render_template('main.html', posts=blog_app.posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post_page():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_app.create_post(session['username'], title, content)
        return redirect('/main')
    return render_template('new_post.html')

@app.route('/view_post/<title>')
def view_post(title):
    post = next((p for p in blog_app.posts if p.title == title), None)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<title>', methods=['GET', 'POST'])
def edit_post(title):
    if request.method == 'POST':
        new_content = request.form['content']
        blog_app.edit_post(session['username'], title, new_content)
        return redirect('/main')
    post = next((p for p in blog_app.posts if p.title == title), None)
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<title>')
def delete_post(title):
    blog_app.delete_post(title)
    return redirect('/main')

if __name__ == '__main__':
    app.run(port=8478, debug=False)
