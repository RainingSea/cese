from flask import Flask, render_template, request, redirect, session
from flask_session import Session

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.tip_manager = TipManager()
        self.resource_manager = ResourceManager()
        self.forum_manager = ForumManager()

    def main(self):
        app = Flask(__name__)
        app.secret_key = 'your_secret_key'
        app.config['SESSION_TYPE'] = 'filesystem'
        Session(app)

        @app.route('/', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                if self.user_manager.login(username, password):
                    session['username'] = username
                    return redirect('/dashboard')
            return render_template('login.html')

        @app.route('/dashboard')
        def dashboard():
            tips = self.tip_manager.get_tips()
            return render_template('dashboard.html', tips=tips)

        @app.route('/create_account', methods=['GET', 'POST'])
        def create_account():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                self.user_manager.create_account(username, password)
                return redirect('/')
            return render_template('create_account.html')

        @app.route('/submit_tip', methods=['POST'])
        def submit_tip():
            tip = request.form['tip']
            self.tip_manager.submit_tip(tip)
            return redirect('/dashboard')

        @app.route('/resources')
        def resources():
            resources = self.resource_manager.get_resources()
            return render_template('resources.html', resources=resources)

        @app.route('/forum', methods=['GET', 'POST'])
        def forum():
            if request.method == 'POST':
                post = request.form['post']
                self.forum_manager.add_post(post)
                return redirect('/forum')
            posts = self.forum_manager.get_posts()
            return render_template('forum.html', posts=posts)

        @app.route('/profile')
        def profile():
            return render_template('profile.html')

        @app.route('/contact')
        def contact():
            return render_template('contact.html')

        app.run(port=8327, debug=False)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def create_account(self, username: str, password: str) -> bool:
        if username not in self.users:
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}\n")
            self.users[username] = password
            return True
        return False

class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        with open('tips.txt', 'r') as file:
            return [line.strip() for line in file]

    def get_tips(self) -> list:
        return self.tips

    def submit_tip(self, tip: str) -> bool:
        with open('tips.txt', 'a') as file:
            file.write(tip + '\n')
        self.tips.append(tip)
        return True

class ResourceManager:
    def __init__(self):
        self.resources = self.load_resources()

    def load_resources(self):
        with open('resources.txt', 'r') as file:
            return [line.strip() for line in file]

    def get_resources(self) -> list:
        return self.resources

    def add_resource(self, resource: str) -> bool:
        with open('resources.txt', 'a') as file:
            file.write(resource + '\n')
        self.resources.append(resource)
        return True

class ForumManager:
    def __init__(self):
        self.posts = self.load_posts()

    def load_posts(self):
        with open('forum.txt', 'r') as file:
            return [line.strip() for line in file]

    def get_posts(self) -> list:
        return self.posts

    def add_post(self, post: str) -> bool:
        with open('forum.txt', 'a') as file:
            file.write(post + '\n')
        self.posts.append(post)
        return True

if __name__ == '__main__':
    main_app = Main()
    main_app.main()