from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from story_manager import StoryManager

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
        user_manager.register(username, password, email)
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/story_creation')
    return redirect('/')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story_manager.create_story(title, content)
        return redirect('/story_creation')
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8164, debug=False)
