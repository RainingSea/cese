from flask import Flask, render_template, request, redirect, url_for, flash
from user_manager import UserManager
from story_manager import StoryManager
from user import User
from story import Story

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
story_manager = StoryManager('stories.txt')

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
        user_manager.save_user(new_user)
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.authenticate(username, password):
        return redirect(url_for('story_creation'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('login'))

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = request.form['username']  # Assume username is passed in the form
        new_story = Story(username, title, content)
        story_manager.save_story(new_story)
        flash('Story saved successfully!')
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8022, debug=False)
