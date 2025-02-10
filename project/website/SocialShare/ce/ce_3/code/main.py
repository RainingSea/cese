from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

class Profile:
    def __init__(self, username: str, bio: str, personal_info: dict):
        self.username = username
        self.bio = bio
        self.personal_info = personal_info

    def update(self, bio: str, personal_info: dict):
        self.bio = bio
        self.personal_info = personal_info
        with open('profiles.txt', 'a') as file:
            json.dump({"username": self.username, "bio": self.bio, "personal_info": self.personal_info}, file)
            file.write("\n")

class Content:
    def __init__(self, username: str, article: str):
        self.username = username
        self.article = article

    def save(self):
        with open('content.txt', 'a') as file:
            json.dump({"username": self.username, "article": self.article}, file)
            file.write("\n")

class SocialShare:
    def __init__(self):
        self.users = self.load_users()
        self.profiles = self.load_profiles()
        self.content = self.load_content()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def load_profiles(self):
        profiles = []
        try:
            with open('profiles.txt', 'r') as file:
                for line in file:
                    profiles.append(json.loads(line.strip()))
        except FileNotFoundError:
            pass
        return profiles

    def load_content(self):
        content = []
        try:
            with open('content.txt', 'r') as file:
                for line in file:
                    content.append(json.loads(line.strip()))
        except FileNotFoundError:
            pass
        return content

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def create_profile(self, username: str, bio: str, personal_info: dict):
        new_profile = Profile(username, bio, personal_info)
        new_profile.update(bio, personal_info)
        self.profiles.append({"username": username, "bio": bio, "personal_info": personal_info})

    def upload_content(self, username: str, article: str):
        new_content = Content(username, article)
        new_content.save()
        self.content.append({"username": username, "article": article})

    def explore_content(self):
        return self.content

social_share = SocialShare()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if social_share.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = session.get('username')
        bio = request.form['bio']
        personal_info = json.loads(request.form['personal_info'])
        social_share.create_profile(username, bio, personal_info)
        return redirect(url_for('feed'))
    return render_template('profile.html')

@app.route('/feed')
def feed():
    content = social_share.explore_content()
    return render_template('feed.html', content=content)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = session.get('username')
        article = request.form['article']
        social_share.upload_content(username, article)
        return redirect(url_for('feed'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(port=8644, debug=False)
