from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from article_manager import ArticleManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

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
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    articles = article_manager.load_articles()
    return render_template('dashboard.html', articles=articles)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/article/<headline>', methods=['GET'])
def article_details(headline):
    if 'username' not in session:
        return redirect(url_for('login'))
    article = article_manager.get_article_details(headline)
    return render_template('article_details.html', article=article)

if __name__ == '__main__':
    app.run(port=8190, debug=False)
