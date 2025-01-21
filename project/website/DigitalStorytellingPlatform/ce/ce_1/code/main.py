from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from story import Story

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split(',')
            users.append(User(username, password, email))
    return users

def load_stories():
    stories = []
    with open('stories.txt', 'r') as file:
        for line in file:
            username, title, content = line.strip().split(',')
            stories.append(Story(username, title, content))
    return stories

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_story = Story(session['username'], title, content)
        new_story.save()
        return redirect(url_for('login'))
    return render_template('story_creation.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.validate_login(username, password):
            session['username'] = username
            return redirect(url_for('story_creation'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8939, debug=False)
