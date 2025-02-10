from flask import Flask, render_template, request, redirect, url_for, flash
from user_manager import UserManager
from story_manager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
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
        if user_manager.register(username, password, email):
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect(url_for('story_creation'))
    else:
        flash('Login failed. Please check your username and password.')
        return redirect(url_for('login'))

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = request.form['username']  # Assuming username is passed in the form
        story_manager.save_story(username, title, content)
        flash('Story saved successfully.')
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8532, debug=False)
