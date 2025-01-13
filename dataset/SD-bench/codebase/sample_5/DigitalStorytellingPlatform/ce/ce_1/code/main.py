from flask import Flask, render_template, request, redirect, url_for
from user import User
from story import Story

app = Flask(__name__)

# Load users and stories from files
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split(',')
            users[username] = (password, email)
    return users

def load_stories():
    stories = []
    with open('stories.txt', 'r') as file:
        for line in file:
            username, title, content = line.strip().split(',')
            stories.append((username, title, content))
    return stories

users = load_users()
stories = load_stories()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password, '')
        if user.login(username, password):
            return redirect(url_for('story_creation'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        if user.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        story = Story(username, title, content)
        story.save_story(username, title, content)
        return redirect(url_for('login'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8449, debug=False)
