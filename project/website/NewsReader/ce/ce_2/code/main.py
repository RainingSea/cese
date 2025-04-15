from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from ArticleManager import ArticleManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
article_manager = ArticleManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login_user(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/do_register', methods=['POST'])
def do_register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register_user(username, password):
        return redirect('/')
    return redirect('/register')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        categories = {article.source for article in article_manager.articles}
        return render_template('dashboard.html', categories=categories)
    return redirect('/')

@app.route('/article/<int:index>')
def article_details(index):
    article = article_manager.get_article(index)
    if article:
        return render_template('article_details.html', article=article)
    return redirect('/dashboard')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = article_manager.search_articles(query)
    if isinstance(results, str):  # Check if results is a message
        return render_template('dashboard.html', message=results)
    return render_template('search_results.html', articles=results)

if __name__ == '__main__':
    app.run(port=8309, debug=False)
