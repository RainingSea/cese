from flask import Flask, render_template, request, redirect, url_for, session, flash
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
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def update_profile(self, username: str, interests: list) -> None:
        # Placeholder for future implementation
        pass

class GroupManager:
    def __init__(self):
        self.groups = self.load_groups()

    def load_groups(self):
        groups = {}
        if os.path.exists('groups.txt'):
            with open('groups.txt', 'r') as file:
                for line in file:
                    name, description = line.strip().split('|')
                    groups[name] = description
        return groups

    def create_group(self, name: str, description: str) -> None:
        self.groups[name] = description
        with open('groups.txt', 'a') as file:
            file.write(f"{name}|{description}\n")

    def join_group(self, username: str, group_name: str) -> str:
        if group_name not in self.groups:
            return "Group does not exist."
        # Placeholder for adding user to group logic
        return f"{username} joined {group_name} successfully."

class ResourceManager:
    def __init__(self):
        self.resources = self.load_resources()

    def load_resources(self):
        resources = []
        if os.path.exists('resources.txt'):
            with open('resources.txt', 'r') as file:
                for line in file:
                    resources.append(line.strip())
        return resources

    def share_resource(self, username: str, resource: str) -> None:
        self.resources.append(resource)
        with open('resources.txt', 'a') as file:
            file.write(f"{username}|{resource}\n")

    def access_resources(self) -> list:
        return self.resources

    def view_resource_details(self, resource: str) -> str:
        # Placeholder for future implementation
        return f"Details of resource: {resource}"

class MessageManager:
    def __init__(self):
        self.messages = self.load_messages()

    def load_messages(self):
        messages = {}
        if os.path.exists('messages.txt'):
            with open('messages.txt', 'r') as file:
                for line in file:
                    group_name, sender, message = line.strip().split('|')
                    if group_name not in messages:
                        messages[group_name] = []
                    messages[group_name].append((sender, message))
        return messages

    def send_message(self, sender: str, group_name: str, message: str) -> str:
        if group_name not in self.messages:
            self.messages[group_name] = []
        self.messages[group_name].append((sender, message))
        with open('messages.txt', 'a') as file:
            file.write(f"{group_name}|{sender}|{message}\n")
        return "Message sent successfully."

    def get_messages(self, group_name: str) -> list:
        return self.messages.get(group_name, [])

user_manager = UserManager()
group_manager = GroupManager()
resource_manager = ResourceManager()
message_manager = MessageManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash("Login failed. Please check your username and password.")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash("Registration successful. Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Registration failed. Username already exists.")
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        flash("You must be logged in to access your profile.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = session.get('username')
        interests = request.form.getlist('interests')
        user_manager.update_profile(username, interests)
        flash("Profile updated successfully.")
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if 'username' not in session:
        flash("You must be logged in to access groups.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        group_name = request.form['group_name']
        join_message = group_manager.join_group(session['username'], group_name)
        flash(join_message)
        return redirect(url_for('groups'))
    return render_template('groups.html', groups=group_manager.groups)

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if 'username' not in session:
        flash("You must be logged in to access resources.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        resource = request.form['resource']
        resource_manager.share_resource(session['username'], resource)
        flash("Resource shared successfully.")
        return redirect(url_for('resources'))
    return render_template('resources.html', resources=resource_manager.access_resources())

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'username' not in session:
        flash("You must be logged in to access messages.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        group_name = request.form['group_name']
        message = request.form['message']
        sender = session.get('username')
        send_message_status = message_manager.send_message(sender, group_name, message)
        flash(send_message_status)
        return redirect(url_for('messages'))
    return render_template('messages.html', messages=message_manager.messages)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8245, debug=False)
