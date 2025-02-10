from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_string(self) -> str:
        return f"{self.username}|{self.password}"

class Tip:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def to_string(self) -> str:
        return f"{self.content}|{self.author}"

class Resource:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link

    def to_string(self) -> str:
        return f"{self.title}|{self.link}"

class ForumPost:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def to_string(self) -> str:
        return f"{self.content}|{self.author}"

class EcoFriendlyLivingTipsApp:
    def __init__(self, users_file: str, tips_file: str, resources_file: str, forum_file: str):
        self.users_file = users_file
        self.tips_file = tips_file
        self.resources_file = resources_file
        self.forum_file = forum_file

    def register_user(self, username: str, password: str) -> bool:
        users = self.load_users()
        if username in [user.username for user in users]:
            return False
        new_user = User(username, password)
        with open(self.users_file, 'a') as f:
            f.write(new_user.to_string() + '\n')
        return True

    def login_user(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def submit_tip(self, content: str, author: str) -> None:
        new_tip = Tip(content, author)
        with open(self.tips_file, 'a') as f:
            f.write(new_tip.to_string() + '\n')

    def add_resource(self, title: str, link: str) -> None:
        new_resource = Resource(title, link)
        with open(self.resources_file, 'a') as f:
            f.write(new_resource.to_string() + '\n')

    def submit_forum_post(self, content: str, author: str) -> None:
        new_post = ForumPost(content, author)
        with open(self.forum_file, 'a') as f:
            f.write(new_post.to_string() + '\n')

    def load_users(self) -> list:
        users = []
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_tips(self) -> list:
        tips = []
        if os.path.exists(self.tips_file):
            with open(self.tips_file, 'r') as f:
                for line in f:
                    content, author = line.strip().split('|')
                    tips.append(Tip(content, author))
        return tips

    def load_resources(self) -> list:
        resources = []
        if os.path.exists(self.resources_file):
            with open(self.resources_file, 'r') as f:
                for line in f:
                    title, link = line.strip().split('|')
                    resources.append(Resource(title, link))
        return resources

    def load_forum_posts(self) -> list:
        posts = []
        if os.path.exists(self.forum_file):
            with open(self.forum_file, 'r') as f:
                for line in f:
                    content, author = line.strip().split('|')
                    posts.append(ForumPost(content, author))
        return posts

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET'])
def home():
    tips = app_instance.load_tips()
    return render_template('home.html', tips=tips)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if app_instance.login_user(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app_instance = EcoFriendlyLivingTipsApp('users.txt', 'tips.txt', 'resources.txt', 'forum.txt')
    app.run(port=8624, debug=False)
