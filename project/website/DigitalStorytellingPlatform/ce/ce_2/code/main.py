from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users[username] = {'password': password, 'email': email}
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'email': email}
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username]['password'] == password:
            session['username'] = username
            return True
        return False

    def save_story(self, username: str, title: str, content: str) -> None:
        with open(f"{username}_stories.txt", 'a') as file:
            file.write(f"{title}|{content}\n")

    def edit_story(self, username: str, title: str, content: str) -> None:
        stories = []
        with open(f"{username}_stories.txt", 'r') as file:
            stories = file.readlines()
        with open(f"{username}_stories.txt", 'w') as file:
            for story in stories:
                if story.startswith(title):
                    file.write(f"{title}|{content}\n")
                else:
                    file.write(story)

user_manager = UserManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('story_creation'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_manager.save_story(session['username'], title, content)
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8325, debug=False)
