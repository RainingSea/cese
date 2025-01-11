from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from StoryManager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
story_manager = StoryManager('stories.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login_user(username, password):
            session['username'] = username
            return redirect('/story_creation')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register_user(username, password, email):
            return redirect('/')
    return render_template('register.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if 'username' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story = Story(session['username'], title, content)
        story_manager.save_story(story)
        return redirect('/story_creation')
    
    stories = story_manager.get_stories(session['username'])
    return render_template('story_creation.html', stories=stories)

if __name__ == '__main__':
    app.run(port=8365, debug=False)
