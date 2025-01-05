from flask import Flask, render_template, request, redirect, url_for, session
from user import User, UserManager
from story import Story, StoryManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
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
        user = User(username, password, email)
        user_manager.save_user(user)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session.get('username')
        story = Story(username, title, content)
        story_manager.save_story(story)
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if user_manager.authenticate(username, password):
        session['username'] = username
        return redirect(url_for('story_creation'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=8021, debug=False)
