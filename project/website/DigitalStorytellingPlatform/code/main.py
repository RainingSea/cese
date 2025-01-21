from flask import Flask, request, redirect, session, render_template
from user import User
from story import Story

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if do_login(username, password):
            return redirect('/story_creation')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    """Handles story creation."""
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_story = Story(session['username'], title, content)
        new_story.save()
        return redirect('/story_creation')
    
    stories = Story.load_stories()
    user_stories = [story for story in stories if story.username == session['username']]
    return render_template('story_creation.html', stories=user_stories)

@app.route('/edit_story/<int:story_id>', methods=['GET', 'POST'])
def edit_story(story_id):
    """Handles story editing."""
    if 'username' not in session:
        return redirect('/')
    
    stories = Story.load_stories()
    user_stories = [story for story in stories if story.username == session['username']]
    
    if story_id < 0 or story_id >= len(user_stories):
        return redirect('/story_creation')
    
    story_to_edit = user_stories[story_id]
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story_to_edit.title = title
        story_to_edit.content = content
        story_to_edit.save()
        return redirect('/story_creation')
    
    return render_template('edit_story.html', story=story_to_edit)

def do_login(username: str, password: str) -> bool:
    """Verifies user credentials and sets session."""
    users = User.load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return True
    return False

if __name__ == '__main__':
    app.run(port=8943, debug=False)
