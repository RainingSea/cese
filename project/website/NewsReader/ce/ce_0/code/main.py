from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
from user import User
from article import Article

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

class NewsReaderApp:
    def __init__(self):
        self.users = User.load_all()
        self.articles = Article.load_all()

    def register(self, username: str, password: str) -> None:
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def browse_news(self) -> List[Article]:
        return self.articles

    def get_article_details(self, headline: str) -> Article:
        for article in self.articles:
            if article.headline == headline:
                return article
        return None

news_reader_app = NewsReaderApp()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if news_reader_app.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        news_reader_app.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    articles = news_reader_app.browse_news()
    return render_template('dashboard.html', articles=articles)

@app.route('/article/<headline>')
def article_details(headline):
    article = news_reader_app.get_article_details(headline)
    return render_template('article_details.html', article=article)

if __name__ == '__main__':
    app.run(port=8652, debug=False)
