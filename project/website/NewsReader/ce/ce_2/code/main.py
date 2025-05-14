from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserAuth:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def register(self, username, password):
        with open(self.users_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.split('|')[0] == username:
                    return False
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class NewsFeed:
    def __init__(self, articles_file='articles.txt', categories_file='categories.txt'):
        self.articles_file = articles_file
        self.categories_file = categories_file
        if not os.path.exists(self.articles_file):
            open(self.articles_file, 'w').close()
        if not os.path.exists(self.categories_file):
            open(self.categories_file, 'w').close()

    def get_articles(self, category=None):
        articles = []
        with open(self.articles_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    article = {
                        'id': parts[0],
                        'title': parts[1],
                        'summary': parts[2],
                        'content': parts[3],
                        'category': parts[4],
                        'source': parts[5]
                    }
                    if not category or article['category'] == category:
                        articles.append(article)
        return articles

    def search_articles(self, query):
        results = []
        with open(self.articles_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    article = {
                        'id': parts[0],
                        'title': parts[1],
                        'summary': parts[2],
                        'content': parts[3],
                        'category': parts[4],
                        'source': parts[5]
                    }
                    if query.lower() in article['title'].lower() or query.lower() in article['summary'].lower():
                        results.append(article)
        return results

    def get_article(self, article_id):
        with open(self.articles_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6 and parts[0] == article_id:
                    return {
                        'id': parts[0],
                        'title': parts[1],
                        'summary': parts[2],
                        'content': parts[3],
                        'category': parts[4],
                        'source': parts[5]
                    }
        return None

    def get_categories(self):
        categories = []
        with open(self.categories_file, 'r') as f:
            for line in f:
                categories.append(line.strip())
        return categories

auth = UserAuth()
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
        if auth.register(username, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    category = request.args.get('category')
    query = request.args.get('query')
    
    if query:
        articles = news_feed.search_articles(query)
    else:
        articles = news_feed.get_articles(category)
    
    categories = news_feed.get_categories()
    return render_template('dashboard.html', 
                          username=session['username'],
                          articles=articles,
                          categories=categories,
                          selected_category=category)

@app.route('/article/<article_id>')
def article(article_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    article = news_feed.get_article(article_id)
    if not article:
        flash('Article not found!', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('article.html', article=article)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8093, debug=False)
