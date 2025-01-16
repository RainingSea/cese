from flask import Flask, render_template, request, redirect, session, flash
from UserManager import UserManager
from StoryManager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
story_manager = StoryManager()

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
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Username already exists. Please choose another one.')
    return render_template('register.html')

@app.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story_manager.create_story(session['username'], title, content)
        flash('Story created successfully!')
        return redirect('/view_stories')
    return render_template('create_story.html')

@app.route('/edit_story/<title>', methods=['GET', 'POST'])
def edit_story(title):
    if 'username' not in session:
        return redirect('/')
    story = story_manager.get_story_by_title(session['username'], title)
    if request.method == 'POST':
        new_content = request.form['content']
        story_manager.edit_story(session['username'], title, new_content)
        flash('Story updated successfully!')
        return redirect('/view_stories')
    return render_template('edit_story.html', story=story)

@app.route('/view_stories')
def view_stories():
    if 'username' not in session:
        return redirect('/')
    stories = story_manager.get_all_stories()
    return render_template('view_stories.html', stories=stories)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/create_story')
    flash('Invalid username or password.')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8453, debug=False)
