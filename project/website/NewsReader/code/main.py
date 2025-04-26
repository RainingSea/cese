from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from article_manager import ArticleManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
article_manager = ArticleManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message = user_manager.add_user(username, password)
        if success:
            return redirect('/')
        else:
            return render_template('register.html', error=message)
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    articles = article_manager.articles
    if not articles:
        return render_template('dashboard.html', articles=[], message="No articles available.")
    return render_template('dashboard.html', articles=articles)

@app.route('/article/<int:article_id>')
def article_details(article_id):
    article = article_manager.get_article_details(article_id)
    if article[0] == "Article not found.":
        return article[0], 404
    return render_template('article_details.html', article=article)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.validate_user(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return render_template('login.html', error="Invalid credentials.")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')