from flask import Flask, render_template, request, redirect, url_for, flash
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
            title, content, author = line.strip().split('|')
            stories.append(Story(title, content, author))
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
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_story = Story(title, content, author)
        new_story.save()
        flash('Story created successfully!')
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8450, debug=False)
