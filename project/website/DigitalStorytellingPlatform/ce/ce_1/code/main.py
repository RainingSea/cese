from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from story_manager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
story_manager = StoryManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_manager.register(username, password, email)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/story', methods=['GET', 'POST'])
def story():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session.get('username')
        story_manager.create_story(username, title, content)
        return redirect(url_for('story'))
    return render_template('story_creation.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('story'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8324, debug=False)
