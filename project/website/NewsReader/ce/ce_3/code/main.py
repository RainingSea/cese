from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from article import Article
from auth import Auth
from news_feed import NewsFeed

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Load users and articles from files
users = User.load_users()
articles = Article.load_articles()

auth = Auth(users)
news_feed = NewsFeed(articles)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', articles=news_feed.get_articles('all'))

@app.route('/article/<int:article_id>')
def article_details(article_id):
    article = articles[article_id]
    return render_template('article_details.html', article=article)

if __name__ == '__main__':
    app.run(port=8655, debug=False)
