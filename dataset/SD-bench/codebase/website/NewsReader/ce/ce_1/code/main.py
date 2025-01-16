from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from article_manager import ArticleManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
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
        else:
            return "Registration failed. Username already exists."
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    articles = article_manager.articles
    return render_template('dashboard.html', articles=articles)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Login failed. Check your username and password."

@app.route('/article/<headline>', methods=['GET'])
def article_details(headline):
    article = article_manager.get_article_details(headline)
    return render_template('article_details.html', article=article)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8653, debug=False)
