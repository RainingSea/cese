from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from article_manager import ArticleManager

app = Flask(__name__)
user_manager = UserManager()
article_manager = ArticleManager()

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
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    articles = article_manager.load_articles()
    return render_template('dashboard.html', articles=articles)

@app.route('/article/<int:article_id>')
def article_details(article_id):
    articles = article_manager.load_articles()
    article = articles[article_id]
    return render_template('article_details.html', article=article)

if __name__ == '__main__':
    app.run(port=8356, debug=False)
