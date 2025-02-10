from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from article import Article

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class App:
    def __init__(self):
        self.user = User()
        self.article = Article()

    def run(self):
        app.run(port=8656, debug=False)

    def register(self, username: str, password: str):
        self.user.username = username
        self.user.password = password
        self.user.save()

    def login(self, username: str, password: str) -> bool:
        return self.user.load(username) and self.user.password == password

    def browse_news(self):
        return self.article.load_all()

    def search_article(self, query: str):
        articles = self.article.load_all()
        return [article for article in articles if query.lower() in article.headline.lower()]

    def view_article(self, article_id: int) -> Article:
        articles = self.article.load_all()
        return articles[article_id] if 0 <= article_id < len(articles) else None

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance.register(username, password)
        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard_page():
    articles = app_instance.browse_news()
    return render_template('dashboard.html', articles=articles)

@app.route('/article/<int:article_id>')
def article_page(article_id):
    article = app_instance.view_article(article_id)
    return render_template('article.html', article=article)

if __name__ == '__main__':
    app_instance = App()
    app_instance.run()