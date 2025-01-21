from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from news_manager import NewsManager

app = Flask(__name__)
user_manager = UserManager()
news_manager = NewsManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.save_user({'username': username, 'password': password})
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')

if __name__ == '__main__':
    app.run(port=9038, debug=False)
