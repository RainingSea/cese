from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from article_manager import ArticleManager

app = Flask(__name__)
user_manager = UserManager('users.txt')
article_manager = ArticleManager('articles.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    articles = article_manager.articles
    return render_template('dashboard.html', articles=articles)

@app.route('/article/<int:article_id>')
def article_details(article_id):
    article = article_manager.articles[article_id]
    return render_template('article_details.html', article=article)

if __name__ == '__main__':
    app.run(port=8656, debug=False)
