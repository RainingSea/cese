from flask import Flask, request, render_template, redirect, url_for
from user_manager import UserManager
from tip_manager import TipManager
from article_manager import ArticleManager
from forum_manager import ForumManager

app = Flask(__name__)

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.tip_manager = TipManager()
        self.article_manager = ArticleManager()
        self.forum_manager = ForumManager()

    def main(self) -> str:
        return "Welcome to GreenLivingGuide!"

    def login(self, username: str, password: str) -> bool:
        return self.user_manager.validate_user(username, password)

    def create_account(self, username: str, password: str) -> bool:
        return self.user_manager.add_user(username, password)

    def view_dashboard(self) -> str:
        return render_template('dashboard.html', tips=self.tip_manager.tips, articles=self.article_manager.articles)

    def submit_tip(self, tip: str) -> bool:
        return self.tip_manager.add_tip(tip)

    def submit_article(self, article: str) -> bool:
        return self.article_manager.add_article(article)

    def post_to_forum(self, post: str) -> bool:
        return self.forum_manager.add_post(post)

main_app = Main()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if main_app.login(username, password):
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return main_app.view_dashboard()

@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    tip = request.form['tip']
    main_app.submit_tip(tip)
    return redirect(url_for('dashboard'))

@app.route('/submit_article', methods=['POST'])
def submit_article():
    article = request.form['article']
    main_app.submit_article(article)
    return redirect(url_for('dashboard'))

@app.route('/post_forum', methods=['POST'])
def post_forum():
    post = request.form['post']
    main_app.post_to_forum(post)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8371, debug=False)
