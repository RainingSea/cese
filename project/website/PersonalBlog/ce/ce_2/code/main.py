from flask import Flask, render_template, request, redirect, url_for, session
import os

class PersonalBlogApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'your_secret_key'
        self.users_file = 'users.txt'
        self.posts_file = 'posts.txt'
        self.app.add_url_rule('/', 'login', self.login_page)
        self.app.add_url_rule('/register', 'register', self.register_page, methods=['GET', 'POST'])
        self.app.add_url_rule('/main', 'main', self.main_page)
        self.app.add_url_rule('/new_post', 'new_post', self.new_post_page, methods=['GET', 'POST'])
        self.app.add_url_rule('/view_post/<int:post_id>', 'view_post', self.view_post_page)
        self.app.add_url_rule('/edit_post/<int:post_id>', 'edit_post', self.edit_post_page, methods=['GET', 'POST'])
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                pass
        if not os.path.exists(self.posts_file):
            with open(self.posts_file, 'w') as f:
                pass

    def login_page(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            return self.login(username, password)
        return render_template('login.html')

    def register_page(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            return self.register(username, password, email)
        return render_template('register.html')

    def main_page(self):
        if 'username' not in session:
            return redirect(url_for('login'))
        posts = self.get_posts(session['username'])
        return render_template('main.html', posts=posts)

    def new_post_page(self):
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            return self.create_post(title, content, session['username'])
        return render_template('new_post.html')

    def view_post_page(self, post_id):
        post = self.get_post(post_id)
        return render_template('view_post.html', post=post)

    def edit_post_page(self, post_id):
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            return self.edit_post(post_id, title, content)
        post = self.get_post(post_id)
        return render_template('edit_post.html', post=post)

    def register(self, username: str, password: str, email: str) -> str:
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return redirect(url_for('login'))

    def login(self, username: str, password: str) -> str:
        with open(self.users_file, 'r') as f:
            for line in f:
                user, pwd, _ = line.strip().split('|')
                if user == username and pwd == password:
                    session['username'] = username
                    return redirect(url_for('main'))
        return "Login failed!"

    def create_post(self, title: str, content: str, username: str) -> str:
        post_id = len(self.get_posts(username)) + 1
        with open(self.posts_file, 'a') as f:
            f.write(f"{post_id}|{title}|{content}|{username}\n")
        return redirect(url_for('main'))

    def edit_post(self, post_id: int, title: str, content: str) -> str:
        posts = self.get_all_posts()
        with open(self.posts_file, 'w') as f:
            for post in posts:
                if post['post_id'] == post_id:
                    f.write(f"{post_id}|{title}|{content}|{post['username']}\n")
                else:
                    f.write(f"{post['post_id']}|{post['title']}|{post['content']}|{post['username']}\n")
        return redirect(url_for('main'))

    def delete_post(self, post_id: int) -> str:
        posts = self.get_all_posts()
        with open(self.posts_file, 'w') as f:
            for post in posts:
                if post['post_id'] != post_id:
                    f.write(f"{post['post_id']}|{post['title']}|{post['content']}|{post['username']}\n")
        return redirect(url_for('main'))

    def get_posts(self, username: str) -> list:
        return [post for post in self.get_all_posts() if post['username'] == username]

    def get_post(self, post_id: int) -> dict:
        posts = self.get_all_posts()
        for post in posts:
            if post['post_id'] == post_id:
                return post
        return {}

    def get_all_posts(self) -> list:
        posts = []
        with open(self.posts_file, 'r') as f:
            for line in f:
                post_id, title, content, username = line.strip().split('|')
                posts.append({'post_id': int(post_id), 'title': title, 'content': content, 'username': username})
        return posts

    def run(self):
        app.run(port=8570, debug=False)

if __name__ == '__main__':
    blog_app = PersonalBlogApp()
    blog_app.run()