from flask import Flask, request, render_template, redirect, url_for, session
from UserManager import UserManager
from StoryManager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
user_manager = UserManager()
story_manager = StoryManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('create_story'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        return "Username already exists"
    return render_template('register.html')

@app.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story_manager.create_story(session['username'], title, content)
        return redirect(url_for('create_story'))
    return render_template('story_creation.html')

@app.route('/edit_story', methods=['GET', 'POST'])
def edit_story():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        new_title = request.form['new_title']
        new_content = request.form['new_content']
        story_manager.edit_story(session['username'], title, new_title, new_content)
        return redirect(url_for('create_story'))
    return render_template('edit_story.html')

if __name__ == '__main__':
    app.run(port=8532, debug=False)
