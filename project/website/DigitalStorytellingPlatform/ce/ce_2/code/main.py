from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.story_manager = StoryManager('stories.txt')

    def main(self):
        app.run(port=8161, debug=False)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if app.user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/story', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = request.form['username']  # Assume username is passed from session or form
        app.story_manager.create_story(title, content, username)
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    main_app = Main()
    main_app.main()