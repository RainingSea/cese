from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from article_manager import ArticleManager

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
        registration_result = user_manager.register(username, password)
        if registration_result['success']:
            return redirect(url_for('login'))
        else:
            return render_template('registration.html', error=registration_result['message'])
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    articles = article_manager.load_articles()
    return render_template('dashboard.html', articles=articles)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    login_result = user_manager.login(username, password)
    if login_result['success']:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html', error=login_result['message'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/article/<int:article_id>')
def article_details(article_id):
    article = article_manager.get_article_details(article_id)
    return render_template('article_details.html', article=article)

if __name__ == '__main__':
    app.run(port=8357, debug=False)
