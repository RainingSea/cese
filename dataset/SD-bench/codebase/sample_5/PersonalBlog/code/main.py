from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from post import Post

app = Flask(__name__)
app.secret_key = 'your_secret_key'
blog_app = None

class BlogApp:
    def __init__(self):
        self.users = User.load_users()
        self.posts = Post.load_posts()

    def register(self, username: str, password: str, email: str) -> str:
        new_user = User(username, password, email)
        if new_user.username not in [user.username for user in self.users]:
            new_user.save()
            self.users.append(new_user)  # Update the users list
            return "Registration successful"
        return "Username already exists"

    def login(self, username: str, password: str) -> str:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return "Login successful"
        return "Invalid username or password"

    def logout_user(self) -> str:
        session.clear()
        return "Logout successful"

    def create_post(self, title: str, content: str, username: str) -> str:
        new_post = Post(title, content, username)
        new_post.save()
        self.posts.append(new_post)  # Update the posts list
        return "Post created"

    def view_post(self, post_id: int) -> Post:
        if 0 <= post_id < len(self.posts):
            return self.posts[post_id]
        return None

    def edit_post(self, post_id: int, new_title: str, new_content: str) -> str:
        if 0 <= post_id < len(self.posts):
            self.posts[post_id].edit(new_title, new_content)
            self.save_posts()  # Save posts after editing
            return "Post updated"
        return "Post not found"

    def delete_post(self, post_id: int) -> str:
        if 0 <= post_id < len(self.posts):
            self.posts.pop(post_id)  # Remove the post from the list
            self.save_posts()  # Save posts after deletion
            return "Post deleted"
        return "Post not found"

    def get_all_posts(self) -> list:
        return self.posts

    def save_posts(self) -> None:
        with open('posts.txt', 'w') as f:
            for post in self.posts:
                f.write(f"{post.title}|{post.content}|{post.username}\n")

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        message = blog_app.register(username, password, email)
        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    message = blog_app.login(username, password)
    return redirect(url_for('main_page'))

@app.route('/logout')
def logout():
    message = blog_app.logout_user()
    return redirect(url_for('login_page'))

@app.route('/main')
def main_page():
    posts = blog_app.get_all_posts()
    return render_template('main.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session.get('username')
        message = blog_app.create_post(title, content, username)
        return redirect(url_for('main_page'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = blog_app.view_post(post_id)
    if post is None:
        return "Post not found", 404
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        message = blog_app.edit_post(post_id, new_title, new_content)
        return redirect(url_for('main_page'))
    post = blog_app.view_post(post_id)
    if post is None:
        return "Post not found", 404
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    message = blog_app.delete_post(post_id)
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    blog_app = BlogApp()  # Initialize the BlogApp instance here
    app.run(port=8482, debug=False)
