from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from story import Story

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split('|')
            users.append(User(username, password, email))
    return users

def load_stories():
    stories = []
    with open('stories.txt', 'r') as file:
        for line in file:
            username, title, content = line.strip().split('|')
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
    return render_template('registration.html')

@app.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        new_story = Story(username, title, content)
        new_story.save()
        return redirect(url_for('login'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8941, debug=False)
