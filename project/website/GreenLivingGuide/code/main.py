from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'supersecretkey'
        self.app.config['SESSION_TYPE'] = 'filesystem'
        Session(self.app)

        self.user_manager = UserManager()
        self.article_manager = ArticleManager()
        self.tips_manager = TipsManager()
        self.forum_manager = ForumManager()

        self.app.route('/')(self.login)
        self.app.route('/dashboard')(self.dashboard)
        self.app.route('/login', methods=['POST'])(self.handle_login)
        self.app.route('/register', methods=['POST'])(self.handle_register)
        self.app.route('/logout')(self.logout)

    def main(self) -> str:
        self.user_manager.load_users()
        self.article_manager.load_articles()
        self.tips_manager.load_tips()
        self.forum_manager.load_posts()
        self.app.run(port=8295, debug=False)

    def login(self):
        return render_template('login.html')

    def dashboard(self):
        if 'username' in session:
            return render_template('dashboard.html', tips=self.tips_manager.tips, articles=self.article_manager.articles, posts=self.forum_manager.posts)
        return redirect(url_for('login'))

    def handle_login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if self.user_manager.login(username, password):
                session['username'] = username
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))

    def handle_register(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if self.user_manager.register(username, password):
                return redirect(url_for('login'))
            return redirect(url_for('login'))

    def logout(self):
        session.pop('username', None)
        return redirect(url_for('login'))

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append((username, password))
        except FileNotFoundError:
            print("User file not found. Starting with an empty user list.")

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users:
                file.write(f"{username}|{password}\n")

    def login(self, username: str, password: str) -> bool:
        for user, pwd in self.users:
            if user == username and pwd == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        self.save_users()
        return True

class ArticleManager:
    def __init__(self):
        self.articles = []

    def load_articles(self) -> None:
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    self.articles.append((title, content))
        except FileNotFoundError:
            print("Article file not found. Starting with an empty article list.")

    def save_articles(self) -> None:
        with open('articles.txt', 'w') as file:
            for title, content in self.articles:
                file.write(f"{title}|{content}\n")

    def submit_article(self, title: str, content: str) -> None:
        self.articles.append((title, content))
        self.save_articles()

class TipsManager:
    def __init__(self):
        self.tips = []

    def load_tips(self) -> None:
        try:
            with open('tips.txt', 'r') as file:
                for line in file:
                    self.tips.append(line.strip())
        except FileNotFoundError:
            print("Tips file not found. Starting with an empty tips list.")

    def save_tips(self) -> None:
        with open('tips.txt', 'w') as file:
            for tip in self.tips:
                file.write(f"{tip}\n")

    def submit_tip(self, content: str) -> None:
        self.tips.append(content)
        self.save_tips()

class ForumManager:
    def __init__(self):
        self.posts = []

    def load_posts(self) -> None:
        try:
            with open('forum.txt', 'r') as file:
                for line in file:
                    self.posts.append(line.strip())
        except FileNotFoundError:
            print("Forum file not found. Starting with an empty forum posts list.")

    def save_posts(self) -> None:
        with open('forum.txt', 'w') as file:
            for post in self.posts:
                file.write(f"{post}\n")

    def submit_post(self, content: str) -> None:
        self.posts.append(content)
        self.save_posts()

if __name__ == '__main__':
    app = Main()
    app.main()