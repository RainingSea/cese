from flask import Flask, render_template, request, redirect, url_for, session, json
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

class UserManager:
    def __init__(self):
        self.users_file = 'users.txt'
        self.profiles_file = 'profiles.txt'
        
    def register_user(self, username, password):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        with open(self.profiles_file, 'a') as f:
            f.write(json.dumps({'username': username, 'interests': ''}) + '\n')
    
    def authenticate_user(self, username, password):
        if not os.path.exists(self.users_file):
            return False
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_user, stored_pass = line.strip().split('|')
                if stored_user == username and stored_pass == password:
                    return True
        return False
    
    def update_profile(self, username, interests):
        profiles = []
        updated = False
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, 'r') as f:
                for line in f:
                    profile = json.loads(line)
                    if profile['username'] == username:
                        profile['interests'] = interests
                        updated = True
                    profiles.append(profile)
        
        with open(self.profiles_file, 'w') as f:
            for profile in profiles:
                f.write(json.dumps(profile) + '\n')
        return updated

class GroupManager:
    def __init__(self):
        self.groups_file = 'groups.txt'
        self.messages_file = 'messages.txt'
        
    def create_group(self, group_name, creator):
        if not os.path.exists(self.groups_file):
            groups = []
        else:
            with open(self.groups_file, 'r') as f:
                groups = [json.loads(line) for line in f]
        
        for group in groups:
            if group['name'] == group_name:
                return False
        
        groups.append({'name': group_name, 'members': [creator], 'resources': []})
        with open(self.groups_file, 'w') as f:
            for group in groups:
                f.write(json.dumps(group) + '\n')
        return True
    
    def join_group(self, group_name, username):
        if not os.path.exists(self.groups_file):
            return False
            
        with open(self.groups_file, 'r') as f:
            groups = [json.loads(line) for line in f]
        
        updated = False
        for group in groups:
            if group['name'] == group_name and username not in group['members']:
                group['members'].append(username)
                updated = True
                break
        
        if updated:
            with open(self.groups_file, 'w') as f:
                for group in groups:
                    f.write(json.dumps(group) + '\n')
        return updated
    
    def post_message(self, group_name, sender, message):
        with open(self.messages_file, 'a') as f:
            f.write(json.dumps({
                'group_name': group_name,
                'sender': sender,
                'message': message
            }) + '\n')
        return True

class ResourceManager:
    def __init__(self):
        self.resources_file = 'resources.txt'
        
    def upload_resource(self, title, resource_type, uploader):
        resource_id = len(self.get_resources()) + 1
        with open(self.resources_file, 'a') as f:
            f.write(json.dumps({
                'id': resource_id,
                'title': title,
                'type': resource_type,
                'uploader': uploader
            }) + '\n')
        return resource_id
    
    def get_resources(self):
        if not os.path.exists(self.resources_file):
            return []
        with open(self.resources_file, 'r') as f:
            return [json.loads(line) for line in f]

user_manager = UserManager()
group_manager = GroupManager()
resource_manager = ResourceManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register_user(username, password)
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    resources = resource_manager.get_resources()[-5:]
    
    groups = []
    if os.path.exists(group_manager.groups_file):
        with open(group_manager.groups_file, 'r') as f:
            groups = [json.loads(line) for line in f]
    
    user_groups = [group for group in groups if username in group['members']]
    
    return render_template('dashboard.html', 
                         username=username,
                         groups=user_groups,
                         resources=resources)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        interests = request.form['interests']
        user_manager.update_profile(username, interests)
        return redirect(url_for('dashboard'))
    
    interests = ''
    if os.path.exists(user_manager.profiles_file):
        with open(user_manager.profiles_file, 'r') as f:
            for line in f:
                profile = json.loads(line)
                if profile['username'] == username:
                    interests = profile['interests']
                    break
    
    return render_template('profile.html', interests=interests)

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        group_name = request.form['group_name']
        group_manager.create_group(group_name, username)
        return redirect(url_for('groups'))
    
    all_groups = []
    if os.path.exists(group_manager.groups_file):
        with open(group_manager.groups_file, 'r') as f:
            all_groups = [json.loads(line) for line in f]
    
    return render_template('groups.html', groups=all_groups, username=username)

@app.route('/join_group/<group_name>')
def join_group(group_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    group_manager.join_group(group_name, username)
    return redirect(url_for('groups'))

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        title = request.form['title']
        resource_type = request.form['type']
        resource_manager.upload_resource(title, resource_type, username)
        return redirect(url_for('resources'))
    
    all_resources = resource_manager.get_resources()
    return render_template('resources.html', resources=all_resources)

@app.route('/messages/<group_name>', methods=['GET', 'POST'])
def messages(group_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        message = request.form['message']
        group_manager.post_message(group_name, username, message)
        return redirect(url_for('messages', group_name=group_name))
    
    group_messages = []
    if os.path.exists(group_manager.messages_file):
        with open(group_manager.messages_file, 'r') as f:
            for line in f:
                msg = json.loads(line)
                if msg['group_name'] == group_name:
                    group_messages.append(msg)
    
    return render_template('messages.html', 
                         group_name=group_name,
                         messages=group_messages,
                         username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8048, debug=False)
