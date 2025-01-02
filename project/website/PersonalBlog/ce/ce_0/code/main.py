from flask import Flask, render_template, request, redirect, url_for, session, flash
from typing import List

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password},{self.email}\n")

class BlogPost:
    def __init__(self, post_id: int, title: str, content: str):
        self.post_id = post_id
        self.title = title
        self.content = content

    def save(self):
        with open('posts.txt', 'a') as file:
            file.write(f"{self.post_id},{self.title},{self.content}\n")

    def delete(self):
        posts = self.get_all_posts()
        with open('posts.txt', 'w') as file:
            for post in posts:
                if post.post_id != self.post_id:
                    file.write(f"{post.post_id},{post.title},{post.content}\n")

    @staticmethod
    def get_all_posts() -> List['BlogPost']:
        posts = []
        try:
            with open('posts.txt', 'r') as file:
                for line in file:
                    post_id, title, content = line.strip().split(',')
                    posts.append(BlogPost(int(post_id), title, content))
        except FileNotFoundError:
            pass
        return posts

class BlogApp:
    def __init__(self):
        self.users = self.load_users()
        self.posts = BlogPost.get_all_posts()

    def load_users(self) -> List[User]:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, email)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def create_post(self, title: str, content: str) -> None:
        post_id = len(self.posts) + 1
        new_post = BlogPost(post_id, title, content)
        new_post.save()
        self.posts.append(new_post)

    def edit_post(self, post_id: int, title: str, content: str) -> None:
        for post in self.posts:
            if post.post_id == post_id:
                post.title = title
                post.content = content
                post.delete()  # Remove old post
                post.save()    # Save updated post
                break

    def delete_post(self, post_id: int) -> None:
        for post in self.posts:
            if post.post_id == post_id:
                post.delete()
                self.posts.remove(post)
                break

app = Flask(__name__)
app.secret_key = 'your_secret_key'
blog_app = BlogApp()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if blog_app.login(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if blog_app.register(username, password, email):
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.', 'danger')
    return render_template('register.html')

@app.route('/main')
def main():
    return render_template('main.html', posts=blog_app.posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_app.create_post(title, content)
        flash('Post created successfully!', 'success')
        return redirect(url_for('main'))
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = next((p for p in blog_app.posts if p.post_id == post_id), None)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = next((p for p in blog_app.posts if p.post_id == post_id), None)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_app.edit_post(post_id, title, content)
        flash('Post updated successfully!', 'success')
        return redirect(url_for('view_post', post_id=post_id))
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    blog_app.delete_post(post_id)
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8175, debug=True)
