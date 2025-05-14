from flask import Flask, render_template, request, redirect, url_for, session
from auth import AuthManager
from news_feed import NewsFeed

app = Flask(__name__)
app.secret_key = 'secret_key_here'

auth_manager = AuthManager()
news_feed = NewsFeed()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.register(username, password):
            return redirect(url_for('login'))
        return render_template('registration.html', error="Username already exists")
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    
    if query:
        articles = news_feed.search_articles(query)
    elif category:
        articles = [a for a in news_feed._load_articles() if a['category'] == category]
    else:
        articles = news_feed._load_articles()
    
    categories = news_feed.get_categories()
    return render_template('dashboard.html', 
                         username=session['username'],
                         articles=articles,
                         categories=categories,
                         query=query,
                         selected_category=category)

@app.route('/article/<int:article_id>')
def article(article_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    article = news_feed.get_article_details(article_id)
    if not article:
        return redirect(url_for('dashboard'))
    return render_template('article.html', article=article)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8092, debug=False)
