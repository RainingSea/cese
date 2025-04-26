import os
from UserManager import UserManager
from TipManager import TipManager
from ArticleManager import ArticleManager
from ForumManager import ForumManager
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.tip_manager = TipManager()
        self.article_manager = ArticleManager()
        self.forum_manager = ForumManager()

    def main(self):
        app.run(port=8172, debug=False)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']
    if main_instance.user_manager.login(username, password):
        return render_template('dashboard.html', tips=main_instance.tip_manager.view_tips(),
                               articles=main_instance.article_manager.view_articles(),
                               posts=main_instance.forum_manager.view_posts())
    return redirect(url_for('login'))

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()