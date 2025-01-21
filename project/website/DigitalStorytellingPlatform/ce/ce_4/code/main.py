from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from story import Story

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split('|')
            users[username] = User(username, password, email)
    return users

def load_stories():
    stories = {}
    with open('stories.txt', 'r') as file:
        for line in file:
            username, title, content = line.strip().split('|')
            stories[title] = Story(title, content, username)
    return stories

users = load_users()
stories = load_stories()

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

@app.route('/story', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username')
        new_story = Story(title, content, author)
        new_story.save()
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8942, debug=False)
