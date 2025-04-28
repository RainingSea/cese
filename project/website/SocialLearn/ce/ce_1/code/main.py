from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class ProfileManager:
    def __init__(self, profiles_file: str):
        self.profiles_file = profiles_file
        self.load_profiles()

    def load_profiles(self):
        self.profiles = {}
        try:
            with open(self.profiles_file, 'r') as file:
                for line in file:
                    username, interests = line.strip().split('|')
                    self.profiles[username] = interests
        except FileNotFoundError:
            pass

    def create_profile(self, username: str, interests: str) -> bool:
        if username in self.profiles:
            return False
        self.profiles[username] = interests
        with open(self.profiles_file, 'a') as file:
            file.write(f"{username}|{interests}\n")
        return True

    def update_profile(self, username: str, interests: str) -> bool:
        if username not in self.profiles:
            return False
        self.profiles[username] = interests
        with open(self.profiles_file, 'w') as file:
            for user, interest in self.profiles.items():
                file.write(f"{user}|{interest}\n")
        return True

class ResourceManager:
    def __init__(self, resources_file: str):
        self.resources_file = resources_file
        self.load_resources()

    def load_resources(self):
        self.resources = []
        try:
            with open(self.resources_file, 'r') as file:
                for line in file:
                    self.resources.append(line.strip())
        except FileNotFoundError:
            pass

    def share_resource(self, username: str, resource: str) -> bool:
        self.resources.append(f"{username}|{resource}")
        with open(self.resources_file, 'a') as file:
            file.write(f"{username}|{resource}\n")
        return True

    def access_resources(self) -> list:
        return self.resources

class MessageManager:
    def __init__(self, messages_file: str):
        self.messages_file = messages_file
        self.load_messages()

    def load_messages(self):
        self.messages = {}
        try:
            with open(self.messages_file, 'r') as file:
                for line in file:
                    from_user, to_user, message = line.strip().split('|')
                    if to_user not in self.messages:
                        self.messages[to_user] = []
                    self.messages[to_user].append((from_user, message))
        except FileNotFoundError:
            pass

    def send_message(self, from_user: str, to_user: str, message: str) -> bool:
        if to_user not in self.messages:
            self.messages[to_user] = []
        self.messages[to_user].append((from_user, message))
        with open(self.messages_file, 'a') as file:
            file.write(f"{from_user}|{to_user}|{message}\n")
        return True

    def get_messages(self, username: str) -> list:
        return self.messages.get(username, [])

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager('users.txt')
profile_manager = ProfileManager('profiles.txt')
resource_manager = ResourceManager('resources.txt')
message_manager = MessageManager('messages.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if request.method == 'POST':
        interests = request.form['interests']
        profile_manager.create_profile(username, interests)
    return render_template('profile.html', username=username)

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        resource = request.form['resource']
        resource_manager.share_resource(session['username'], resource)
    return render_template('resources.html', resources=resource_manager.access_resources())

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        to_user = request.form['to_user']
        message = request.form['message']
        message_manager.send_message(session['username'], to_user, message)
    return render_template('messages.html', messages=message_manager.get_messages(session['username']))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8415, debug=False)
