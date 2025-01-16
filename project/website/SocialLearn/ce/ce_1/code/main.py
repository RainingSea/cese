from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from profile_manager import ProfileManager
from group_manager import GroupManager
from resource_manager import ResourceManager
from message_manager import MessageManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
profile_manager = ProfileManager()
group_manager = GroupManager()
resource_manager = ResourceManager()
message_manager = MessageManager()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
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
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    if request.method == 'POST':
        interests = request.form.getlist('interests')
        profile_manager.update_profile(username, interests)
    user_profile = profile_manager.load_profiles()
    return render_template('profile.html', profile=user_profile.get(username, {}))

@app.route('/groups')
def groups():
    available_groups = group_manager.load_groups()
    return render_template('groups.html', groups=available_groups)

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        resource = request.form['resource']
        username = session.get('username')
        resource_manager.share_resource(username, resource)
    shared_resources = resource_manager.load_resources()
    return render_template('resources.html', resources=shared_resources)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        from_user = session.get('username')
        to_user = request.form['to_user']
        message = request.form['message']
        message_manager.send_message(from_user, to_user, message)
    all_messages = message_manager.load_messages()
    return render_template('messages.html', messages=all_messages)

if __name__ == '__main__':
    user_manager.load_users()
    profile_manager.load_profiles()
    group_manager.load_groups()
    resource_manager.load_resources()
    message_manager.load_messages()
    app.run(port=8636, debug=False)
