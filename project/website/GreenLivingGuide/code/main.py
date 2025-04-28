from flask import Flask, render_template, request, redirect, session
from flask_session import Session

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                return True
        return False

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                self.users = [line.strip().split('|') for line in file.readlines()]
        except FileNotFoundError:
            self.users = []

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')


class ArticleManager:
    def __init__(self):
        self.articles = []
        self.load_articles()

    def submit_article(self, title: str, content: str) -> bool:
        self.articles.append((title, content))
        self.save_articles()
        return True

    def load_articles(self) -> None:
        try:
            with open('articles.txt', 'r') as file:
                self.articles = [line.strip().split('|') for line in file.readlines()]
        except FileNotFoundError:
            self.articles = []

    def save_articles(self) -> None:
        with open('articles.txt', 'w') as file:
            for article in self.articles:
                file.write('|'.join(article) + '\n')


class TipManager:
    def __init__(self):
        self.tips = []
        self.load_tips()

    def submit_tip(self, tip: str) -> bool:
        self.tips.append((tip,))
        self.save_tips()
        return True

    def load_tips(self) -> None:
        try:
            with open('tips.txt', 'r') as file:
                self.tips = [line.strip().split('|') for line in file.readlines()]
        except FileNotFoundError:
            self.tips = []

    def save_tips(self) -> None:
        with open('tips.txt', 'w') as file:
            for tip in self.tips:
                file.write('|'.join(tip) + '\n')


class ForumManager:
    def __init__(self):
        self.posts = []
        self.load_posts()

    def submit_post(self, content: str) -> bool:
        self.posts.append((content,))
        self.save_posts()
        return True

    def load_posts(self) -> None:
        try:
            with open('forum.txt', 'r') as file:
                self.posts = [line.strip().split('|') for line in file.readlines()]
        except FileNotFoundError:
            self.posts = []

    def save_posts(self) -> None:
        with open('forum.txt', 'w') as file:
            for post in self.posts:
                file.write('|'.join(post) + '\n')


app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager()
article_manager = ArticleManager()
tip_manager = TipManager()
forum_manager = ForumManager()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect('/dashboard')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tips=tip_manager.tips)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        tip = request.form['tip']
        tip_manager.submit_tip(tip)
    return render_template('tips.html', tips=tip_manager.tips)


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article_manager.submit_article(title, content)
    return render_template('articles.html', articles=article_manager.articles)


@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        forum_manager.submit_post(content)
    return render_template('forum.html', posts=forum_manager.posts)


if __name__ == '__main__':
    app.run(port=8337, debug=False)
