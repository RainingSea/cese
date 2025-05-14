from flask import Flask, render_template, request, redirect, url_for, session, flash
from managers import UserManager, ProfileManager, GroupManager, ResourceManager, MessageManager
import logging
from functools import wraps

app = Flask(__name__)
app.secret_key = 'demo_secret_key'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour session timeout

logging.basicConfig(filename='app.log', level=logging.DEBUG)

user_manager = UserManager('users.txt')
profile_manager = ProfileManager('profiles.txt')
group_manager = GroupManager('groups.txt')
resource_manager = ResourceManager('resources.txt')
message_manager = MessageManager('messages.txt')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login first')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    session.permanent = True

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
        if user_manager.validate_user(username, password):
            session['username'] = username
            flash('Login successful')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.user_exists(username):
            flash('Username already exists')
            return render_template('register.html', username=username)
        if user_manager.register(username, password):
            session['username'] = username
            profile_manager.update_profile(username, '', '')
            flash('Registration successful')
            return redirect(url_for('dashboard'))
        flash('Registration failed')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    user_groups = group_manager.get_user_groups(username)
    latest_resources = resource_manager.get_latest_resources(5)
    return render_template('dashboard.html',
                         username=username,
                         groups=user_groups,
                         resources=latest_resources)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = session['username']
    if request.method == 'POST':
        interests = request.form['interests']
        expertise = request.form['expertise']
        if profile_manager.update_profile(username, interests, expertise):
            flash('Profile updated successfully')
            return redirect(url_for('dashboard'))
        flash('Failed to update profile')
    profile_data = profile_manager.get_profile(username)
    return render_template('profile.html', profile=profile_data)

@app.route('/groups')
@login_required
def groups():
    username = session['username']
    all_groups = group_manager.list_groups()
    user_groups = group_manager.get_user_groups(username)
    return render_template('groups.html',
                         groups=all_groups,
                         user_groups=user_groups,
                         username=username)

@app.route('/join_group/<groupname>')
@login_required
def join_group(groupname):
    username = session['username']
    if group_manager.join_group(username, groupname):
        flash(f'Successfully joined {groupname}')
    else:
        flash(f'Failed to join {groupname}')
    return redirect(url_for('groups'))

@app.route('/group_messages/<groupname>', methods=['GET', 'POST'])
@login_required
def group_messages(groupname):
    username = session['username']
    if request.method == 'POST':
        message = request.form['message']
        if message_manager.post_group_message(groupname, username, message):
            flash('Message posted successfully')
        else:
            flash('Failed to post message')
    messages = message_manager.get_group_messages(groupname)
    return render_template('group_messages.html',
                         groupname=groupname,
                         messages=messages,
                         username=username)

@app.route('/resources', methods=['GET', 'POST'])
@login_required
def resources():
    username = session['username']
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        group = request.form['group']
        if resource_manager.add_resource(title, content, username, group):
            flash('Resource added successfully')
        else:
            flash('Failed to add resource')
    all_resources = resource_manager.get_resources(None)
    return render_template('resources.html',
                         resources=all_resources,
                         username=username)

@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    username = session['username']
    if request.method == 'POST':
        receiver = request.form['receiver']
        content = request.form['content']
        if message_manager.send_message(username, receiver, content):
            flash('Message sent successfully')
        else:
            flash('Failed to send message')
    user_messages = message_manager.get_messages(username)
    return render_template('messages.html',
                         messages=user_messages,
                         username=username)

if __name__ == '__main__':
    app.run(port=8051, debug=False)
