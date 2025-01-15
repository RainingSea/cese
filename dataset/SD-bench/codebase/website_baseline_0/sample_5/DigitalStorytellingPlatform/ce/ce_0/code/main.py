import logging
import socket
from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from story_manager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
user_manager = UserManager('users.txt')
story_manager = StoryManager('stories.txt')

def is_port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

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
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('story_creation'))
    return redirect(url_for('login'))

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        try:
            validate_input(title, content)
            story = Story(session['username'], title, content)
            story_manager.save_story(story)
            return redirect(url_for('story_creation'))
        except ValueError as e:
            logging.error("Input validation error: %s", e)
            return render_template('story_creation.html', error=str(e))
    return render_template('story_creation.html')

def validate_input(title: str, content: str) -> None:
    if not title or not content:
        raise ValueError("Title and content must not be empty.")

if __name__ == '__main__':
    try:
        if is_port_available(8068):
            app.run(port=8068, debug=False)
        else:
            logging.error("Port 8068 is already in use. Please choose another port.")
            exit(1)
    except Exception as e:
        logging.error("Failed to start application: %s", e)
        exit(1)