from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, filename='users.txt'):
        self.filename = filename
    
    def validate_user(self, username, password):
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    stored_username, stored_password = line.strip().split(',')
                    if username == stored_username and password == stored_password:
                        return True
        except FileNotFoundError:
            return False
        return False
    
    def create_user(self, username, password):
        try:
            with open(self.filename, 'a+') as f:
                f.seek(0)
                for line in f:
                    stored_username, _ = line.strip().split(',')
                    if username == stored_username:
                        return False
                f.write(f"{username},{password}\n")
                return True
        except:
            return False

class ProfileManager:
    def __init__(self, filename='profiles.txt'):
        self.filename = filename
    
    def get_profile(self, username):
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if parts[0] == username:
                        return {'username': parts[0], 'interests': parts[1:]}
        except FileNotFoundError:
            return None
        return None
    
    def update_profile(self, username, interests):
        try:
            lines = []
            updated = False
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if parts[0] == username:
                        lines.append(f"{username},{interests}\n")
                        updated = True
                    else:
                        lines.append(line)
            
            if not updated:
                lines.append(f"{username},{interests}\n")
            
            with open(self.filename, 'w') as f:
                f.writelines(lines)
            return True
        except:
            return False

class GroupManager:
    def __init__(self, filename='groups.txt'):
        self.filename = filename
    
    def get_groups(self):
        groups = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    groups.append({
                        'name': parts[0],
                        'members': parts[1:]
                    })
        except FileNotFoundError:
            pass
        return groups
    
    def join_group(self, username, group_name):
        try:
            lines = []
            updated = False
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if parts[0] == group_name:
                        if username not in parts[1:]:
                            parts.append(username)
                            lines.append(','.join(parts) + '\n')
                            updated = True
                        else:
                            lines.append(line)
                    else:
                        lines.append(line)
            
            if not updated:
                lines.append(f"{group_name},{username}\n")
            
            with open(self.filename, 'w') as f:
                f.writelines(lines)
            return True
        except:
            return False

class ResourceManager:
    def __init__(self, filename='resources.txt'):
        self.filename = filename
    
    def share_resource(self, title, type, link, shared_by):
        try:
            with open(self.filename, 'a') as f:
                f.write(f"{title},{type},{link},{shared_by}\n")
            return True
        except:
            return False
    
    def get_resources(self):
        resources = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    resources.append({
                        'title': parts[0],
                        'type': parts[1],
                        'link': parts[2],
                        'shared_by': parts[3]
                    })
        except FileNotFoundError:
            pass
        return resources

class MessageManager:
    def __init__(self, filename='messages.txt'):
        self.filename = filename
    
    def send_message(self, sender, receiver, content):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.filename, 'a') as f:
                f.write(f"{sender},{receiver},{content},{timestamp}\n")
            return True
        except:
            return False
    
    def get_messages(self, user):
        messages = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if parts[0] == user or parts[1] == user:
                        messages.append({
                            'sender': parts[0],
                            'receiver': parts[1],
                            'content': parts[2],
                            'timestamp': parts[3]
                        })
        except FileNotFoundError:
            pass
        return messages

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager = UserManager()
        if user_manager.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager = UserManager()
        if user_manager.create_user(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    profile_manager = ProfileManager()
    if request.method == 'POST':
        interests = request.form['interests']
        if profile_manager.update_profile(session['username'], interests):
            return redirect(url_for('dashboard'))
    
    user_profile = profile_manager.get_profile(session['username'])
    interests = ','.join(user_profile['interests']) if user_profile else ''
    return render_template('profile.html', interests=interests)

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    group_manager = GroupManager()
    if request.method == 'POST':
        group_name = request.form['group_name']
        group_manager.join_group(session['username'], group_name)
    
    groups = group_manager.get_groups()
    return render_template('groups.html', groups=groups)

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    resource_manager = ResourceManager()
    if request.method == 'POST':
        title = request.form['title']
        type = request.form['type']
        link = request.form['link']
        resource_manager.share_resource(title, type, link, session['username'])
    
    resources = resource_manager.get_resources()
    return render_template('resources.html', resources=resources)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message_manager = MessageManager()
    if request.method == 'POST':
        receiver = request.form['receiver']
        content = request.form['content']
        message_manager.send_message(session['username'], receiver, content)
    
    messages = message_manager.get_messages(session['username'])
    return render_template('messages.html', messages=messages)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8049, debug=False)
