from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from story_manager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
story_manager = StoryManager('stories.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/create_story')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect('/')
    return render_template('register.html')

@app.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story_manager.create_story(title, content)
        return redirect('/create_story')
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8165, debug=False)
