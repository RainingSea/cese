from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # For session management

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Story:
    def __init__(self, id: int, title: str, content: str, cultural_background: str):
        self.id = id
        self.title = title
        self.content = content
        self.cultural_background = cultural_background

def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_stories():
    stories = []
    if os.path.exists('stories.txt'):
        with open('stories.txt', 'r') as file:
            for line in file:
                id, title, content, cultural_background = line.strip().split('|')
                stories.append(Story(int(id), title, content, cultural_background))
    return stories

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    stories = load_stories()
    return render_template('dashboard.html', stories=stories)

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect('/dashboard')
    return redirect('/')

@app.route('/story/<int:story_id>')
def story_details(story_id):
    stories = load_stories()
    for story in stories:
        if story.id == story_id:
            return render_template('story_details.html', story=story)
    return redirect('/dashboard')

@app.route('/bookmark/<int:story_id>')
def bookmark_story(story_id):
    if 'username' in session:
        with open(f"{session['username']}_bookmarks.txt", 'a') as file:
            file.write(f"{story_id}\n")
    return redirect('/dashboard')

@app.route('/bookmarks')
def bookmarks():
    if 'username' in session:
        bookmarked_stories = []
        if os.path.exists(f"{session['username']}_bookmarks.txt"):
            with open(f"{session['username']}_bookmarks.txt", 'r') as file:
                bookmarked_ids = [int(line.strip()) for line in file]
                stories = load_stories()
                for story in stories:
                    if story.id in bookmarked_ids:
                        bookmarked_stories.append(story)
        return render_template('bookmarks.html', stories=bookmarked_stories)
    return redirect('/')

@app.route('/logout')
def logout_user():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=9012, debug=False)
