from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from user_manager import UserManager
from group_manager import GroupManager
from resource_manager import ResourceManager
from message_manager import MessageManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

user_manager = UserManager()
group_manager = GroupManager()
resource_manager = ResourceManager()
message_manager = MessageManager()

@login_manager.user_loader
def load_user(username):
    return user_manager.get_user(username)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        interests = request.form.getlist('interests')
        user_manager.update_profile(current_user.username, interests)
    return render_template('profile.html')

@app.route('/study_groups')
@login_required
def study_groups():
    return render_template('study_groups.html', groups=group_manager.get_groups())

@app.route('/resources')
@login_required
def resources():
    return render_template('resources.html', resources=resource_manager.get_resources())

@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html', messages=message_manager.get_messages(current_user.username))

if __name__ == '__main__':
    app.run(port=8244, debug=False)
