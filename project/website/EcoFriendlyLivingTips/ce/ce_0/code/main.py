from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def create_account(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    def login(self):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username and user_data[1] == self.password:
                    return True
        return False

    def update_profile(self, new_email):
        self.email = new_email
        # Update the users.txt file
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username:
                    users.append(f"{self.username}|{self.password}|{self.email}\n")
                else:
                    users.append(line)
        with open('users.txt', 'w') as f:
            f.writelines(users)

class Tip:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def submit_tip(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

class Resource:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def add_resource(self):
        with open('resources.txt', 'a') as f:
            f.write(f"{self.title}|{self.link}\n")

class ForumPost:
    def __init__(self, username, content):
        self.username = username
        self.content = content

    def create_post(self):
        with open('forum.txt', 'a') as f:
            f.write(f"{self.username}|{self.content}\n")

@login_manager.user_loader
def load_user(username):
    with open('users.txt', 'r') as f:
        for line in f:
            user_data = line.strip().split('|')
            if user_data[0] == username:
                return User(user_data[0], user_data[1], user_data[2])
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password, "")
        if user.login():
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8163, debug=False)
