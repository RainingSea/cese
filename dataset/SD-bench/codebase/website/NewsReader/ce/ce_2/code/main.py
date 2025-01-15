from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from ArticleManager import ArticleManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
article_manager = ArticleManager('articles.txt')

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
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        search_query = request.form['search']
        articles = article_manager.load_articles()
        filtered_articles = [article for article in articles if search_query.lower() in article.lower()]
        return render_template('dashboard.html', articles=filtered_articles)
    articles = article_manager.load_articles()
    return render_template('dashboard.html', articles=articles)

@app.route('/article/<title>')
def article_details(title):
    details = article_manager.get_article_details(title)
    return render_template('article_details.html', details=details)

if __name__ == '__main__':
    app.run(port=8654, debug=False)
