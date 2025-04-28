from flask import Flask, render_template, request, redirect, session
from flask_session import Session

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                headline, summary, source, full_text = line.strip().split(',')
                articles.append({
                    'headline': headline,
                    'summary': summary,
                    'source': source,
                    'full_text': full_text
                })
        return articles

    def search_articles(self, query: str) -> list:
        return [article for article in self.articles if query.lower() in article['headline'].lower()]

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'supersecretkey'
        self.app.config['SESSION_TYPE'] = 'filesystem'
        Session(self.app)
        self.user_manager = UserManager()
        self.article_manager = ArticleManager()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                if self.user_manager.login(username, password):
                    session['username'] = username
                    return redirect('/dashboard')
            return render_template('login.html')

        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                if self.user_manager.register(username, password):
                    return redirect('/')
            return render_template('registration.html')

        @self.app.route('/dashboard')
        def dashboard():
            articles = self.article_manager.articles
            return render_template('dashboard.html', articles=articles)

        @self.app.route('/article/<int:article_id>')
        def article_details(article_id):
            article = self.article_manager.articles[article_id]
            return render_template('article_details.html', article=article)

    def main(self) -> str:
        self.app.run(port=8354, debug=False)

if __name__ == '__main__':
    main_app = Main()
    main_app.main()