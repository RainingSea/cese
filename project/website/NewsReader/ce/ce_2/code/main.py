from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class ArticleManager:
    def __init__(self):
        self.articles = []
        self.load_articles()

    def load_articles(self) -> None:
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as file:
                for line in file:
                    self.articles.append(line.strip())

    def search_articles(self, query: str) -> list:
        return [article for article in self.articles if query.lower() in article.lower()]

    def get_article_details(self, article_id: int) -> str:
        return self.articles[article_id] if 0 <= article_id < len(self.articles) else "Article not found."

user_manager = UserManager()
article_manager = ArticleManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed. User already exists."
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        query = request.form['query']
        search_results = article_manager.search_articles(query)
        return render_template('dashboard.html', articles=search_results)
    return render_template('dashboard.html', articles=article_manager.articles)

@app.route('/article/<int:article_id>')
def article_details(article_id):
    details = article_manager.get_article_details(article_id)
    return render_template('article_details.html', details=details)

if __name__ == '__main__':
    app.run(port=8192, debug=False)
