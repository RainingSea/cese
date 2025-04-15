from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from ArticleManager import ArticleManager
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = UserManager('users.txt')
article_manager = ArticleManager('articles.txt')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        categories = {article.source for article in article_manager.articles}
        return render_template('dashboard.html', categories=categories)
    return redirect('/')

@app.route('/article/<int:article_id>')
def article_details(article_id):
    if 'username' in session:
        if 0 <= article_id < len(article_manager.articles):
            article = article_manager.articles[article_id]
            return render_template('article_details.html', article=article)
    return redirect('/')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    results = article_manager.search_articles(keyword)
    return render_template('search_results.html', results=results)

if __name__ == '__main__':
    app.run(port=8305, debug=False)
