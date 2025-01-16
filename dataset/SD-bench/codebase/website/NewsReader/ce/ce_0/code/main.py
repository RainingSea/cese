from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from article import Article

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class NewsReaderApp:
    def __init__(self):
        self.users = self.load_users()
        self.articles = self.load_articles()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def load_articles(self):
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                headline, summary, source, full_text = line.strip().split('|')
                articles.append(Article(headline, summary, source, full_text))
        return articles

    def register(self, username, password):
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username, password):
        return any(user.username == username and user.password == password for user in self.users)

    def browse_articles(self):
        return self.articles

    def get_article_details(self, headline):
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
        if news_reader_app.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    articles = news_reader_app.browse_articles()
    return render_template('dashboard.html', articles=articles)

@app.route('/article/<headline>')
def article_details(headline):
    article = news_reader_app.get_article_details(headline)
    return render_template('article_details.html', article=article)

if __name__ == '__main__':
    app.run(port=8652, debug=False)
