from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from article import Article
from file_manager import FileManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
file_manager = FileManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register():
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    articles = Article().get_articles()
    return render_template('dashboard.html', articles=articles)

@app.route('/article/<int:article_id>', methods=['GET'])
def article_details(article_id):
    articles = Article().get_articles()
    if 0 <= article_id < len(articles):
        article = articles[article_id]
        return render_template('article_details.html', article=article)
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login():
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8654, debug=False)
