from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None

@login_manager.user_loader
def load_user(username):
    return User.load(username)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.load(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/tips', methods=['GET', 'POST'])
@login_required
def tips():
    if request.method == 'POST':
        tip_content = request.form['tip']
        tip = Tip(tip_content)
        tip.save()
    return render_template('tips.html')

@app.route('/articles', methods=['GET', 'POST'])
@login_required
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = Article(title, content)
        article.save()
    return render_template('articles.html')

@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    if request.method == 'POST':
        username = session['user_id']
        content = request.form['content']
        post = ForumPost(username, content)
        post.save()
    return render_template('forum.html')

if __name__ == '__main__':
    app.run(port=8172, debug=False)
