from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from StoryManager import StoryManager

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
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story_manager.create_story(session['username'], title, content)
        return redirect(url_for('story_creation'))
    
    return render_template('story_creation.html')

@app.route('/edit_story/<title>', methods=['GET', 'POST'])
def edit_story(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_content = request.form['content']
        story_manager.edit_story(session['username'], title, new_content)
        return redirect(url_for('story_creation'))
    
    story = story_manager.get_story(session['username'], title)
    return render_template('edit_story.html', story=story)

if __name__ == '__main__':
    app.run(port=8456, debug=False)
