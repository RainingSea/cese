from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from content_manager import ContentManager

app = Flask(__name__)

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.content_manager = ContentManager()

    def main(self):
        return app.run(debug=True)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if Main().user_manager.register(username, password):
        return redirect(url_for('login'))
    return "Registration failed", 400

@app.route('/home')
def home():
    return render_template('home.html', articles=Main().content_manager.articles)

if __name__ == '__main__':
    Main().main()