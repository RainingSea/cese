from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from story_manager import StoryManager
from user import User
from story import Story

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

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
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    if user_manager.authenticate(username, password):
        session['username'] = username
        return redirect(url_for('story_creation'))
    return "Invalid credentials, please try again."

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_story = Story(session['username'], title, content)
        story_manager.save_story(new_story)
        return redirect(url_for('story_creation'))

    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8020, debug=False)
