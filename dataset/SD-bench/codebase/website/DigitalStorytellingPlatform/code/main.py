from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from StoryManager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
story_manager = StoryManager('stories.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/create_story')
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_manager.register(username, password, email)
        return redirect('/')
    return render_template('register.html')

@app.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story = Story(title, content, session['username'])
        story_manager.save_story(story)
        return redirect('/create_story')
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8305, debug=False)
