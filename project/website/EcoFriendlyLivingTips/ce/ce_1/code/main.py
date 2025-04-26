from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def create_account(username: str, password: str):
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")

    @staticmethod
    def login(username: str, password: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user, pwd = line.strip().split('|')
                if user == username and pwd == password:
                    return True
        return False

class Tip:
    def __init__(self, content):
        self.content = content

    @staticmethod
    def submit_tip(content: str):
        with open('tips.txt', 'a') as f:
            f.write(f"{content}\n")

class Resource:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def add_resource(url: str):
        with open('resources.txt', 'a') as f:
            f.write(f"{url}\n")

class ForumPost:
    def __init__(self, content):
        self.content = content

    @staticmethod
    def create_post(content: str):
        with open('forum.txt', 'a') as f:
            f.write(f"{content}\n")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.login(username, password):
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create_account(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(port=8164, debug=False)
