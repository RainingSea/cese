from flask import Flask, render_template, request, redirect, url_for
from UserManager import UserManager
from ArticleManager import ArticleManager

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
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('registration.html', error='Username already exists')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    categories = article_manager.get_articles('all')
    return render_template('dashboard.html', categories=categories)

@app.route('/article/<article_id>')
def article_details(article_id):
    article = article_manager.get_article_details(article_id)
    return render_template('article_details.html', article=article)

if __name__ == '__main__':
    app.run(port=8355, debug=False)
