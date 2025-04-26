from flask import Flask, render_template, request, redirect, session
from flask_session import Session

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

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                articles.append(line.strip())
        return articles

    def search_articles(self, query: str):
        return [article for article in self.articles if query.lower() in article.lower()]

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager()
article_manager = ArticleManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        return "User already exists", 400
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    articles = article_manager.articles
    return render_template('dashboard.html', articles=articles)

@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = article_manager.articles
    if 0 <= article_id < len(articles):
        return render_template('article_details.html', article=articles[article_id])
    return "Article not found", 404

if __name__ == '__main__':
    app.run(port=8191, debug=False)
