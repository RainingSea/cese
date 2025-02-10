from flask import Flask, render_template, request, redirect, url_for, flash
from user import User
from story import Story
from auth import Auth

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load users and stories from files
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

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        auth = Auth()
        if auth.login(username, password):
            flash('Login successful!', 'success')
            return redirect(url_for('story_creation'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        auth = Auth()
        if auth.register(username, password, email):
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.', 'danger')
    return render_template('registration.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        story = Story(username, title, content)
        story.save_story()
        flash('Story saved successfully!', 'success')
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8531, debug=False)
