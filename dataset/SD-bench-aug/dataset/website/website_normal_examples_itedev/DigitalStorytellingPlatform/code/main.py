from flask import Flask, render_template, request, redirect, url_for, session
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
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        story_manager.create_story(title, content, author)
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html', stories=story_manager.stories)

@app.route('/edit_story/<title>', methods=['GET', 'POST'])
def edit_story(title):
    if request.method == 'POST':
        content = request.form['content']
        story_manager.edit_story(title, content)
        return redirect(url_for('story_creation'))
    story = next((s for s in story_manager.stories if s.title == title), None)
    return render_template('edit_story.html', story=story)

if __name__ == '__main__':
    app.run(debug=True)