from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from ArticleManager import ArticleManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
article_manager = ArticleManager()

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        return "Registration failed. Username may already exist."
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect('/dashboard')
    return "Login failed. Invalid username or password."

@app.route('/dashboard')
def dashboard():
    """Render the dashboard page with articles."""
    if 'username' in session:
        return render_template('dashboard.html', articles=article_manager.articles)
    return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect('/')

@app.route('/article/<int:article_id>')
def article_details(article_id):
    """Render the article details page."""
    if 'username' in session and 0 <= article_id < len(article_manager.articles):
        article = article_manager.articles[article_id]
        return render_template('article_details.html', article=article)
    return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle article search."""
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = article_manager.search_articles(keyword)
        return render_template('search_results.html', articles=results)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(port=8311, debug=False)
