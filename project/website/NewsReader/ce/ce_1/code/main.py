from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from ArticleManager import ArticleManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
article_manager = ArticleManager()

@app.route('/')
def home():
    """Render the login page."""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login_user(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    """Handle user registration."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.register_user(username, password):
        return redirect('/')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    """Render the dashboard page with articles."""
    if 'username' in session:
        return render_template('dashboard.html', articles=article_manager.articles)
    return redirect('/')

@app.route('/article/<title>')
def article_details(title):
    """Render the article details page."""
    article = article_manager.get_article_details(title)
    if article:
        return render_template('article_details.html', article=article)
    return "Article not found", 404

@app.route('/search', methods=['GET'])
def search():
    """Search for articles based on a query."""
    query = request.args.get('query')
    results = article_manager.search_articles(query)
    if not results:
        return render_template('search_results.html', message="No articles found.")
    return render_template('search_results.html', articles=results)

if __name__ == '__main__':
    app.run(port=8307, debug=False)
