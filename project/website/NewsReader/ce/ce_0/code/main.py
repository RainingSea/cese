from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

class NewsReader:
    def __init__(self):
        self.users_file = 'users.txt'
        self.news_file = 'news.txt'
        self.categories_file = 'categories.txt'

    def register_user(self, username, password):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def authenticate(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_user, stored_pass = line.strip().split('|')
                if stored_user == username and stored_pass == password:
                    return True
        return False

    def get_news(self, category=None):
        news_items = []
        with open(self.news_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    if not category or parts[4] == category:
                        news_items.append({
                            'id': parts[0],
                            'title': parts[1],
                            'summary': parts[2],
                            'content': parts[3],
                            'category': parts[4],
                            'source': parts[5]
                        })
        return news_items

    def search_news(self, query):
        results = []
        with open(self.news_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    if query.lower() in parts[1].lower() or query.lower() in parts[2].lower():
                        results.append({
                            'id': parts[0],
                            'title': parts[1],
                            'summary': parts[2],
                            'content': parts[3],
                            'category': parts[4],
                            'source': parts[5]
                        })
        return results

    def get_article(self, article_id):
        with open(self.news_file, 'r') as f:
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

app = Flask(__name__)
app.secret_key = 'secret_key'
news_reader = NewsReader()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if news_reader.authenticate(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        news_reader.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    category = request.args.get('category')
    query = request.args.get('query')
    
    if query:
        news_items = news_reader.search_news(query)
    else:
        news_items = news_reader.get_news(category)
    
    categories = news_reader.get_categories()
    return render_template('dashboard.html', 
                         username=session['username'],
                         news_items=news_items,
                         categories=categories,
                         selected_category=category)

@app.route('/article/<article_id>')
def article(article_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    article = news_reader.get_article(article_id)
    if not article:
        return redirect(url_for('dashboard'))
    return render_template('article.html', article=article)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8091, debug=False)
