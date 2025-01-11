from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from project_manager import ProjectManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
project_manager = ProjectManager('projects.txt')

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

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return render_template('home.html', projects=project_manager.get_all_projects())
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        user_profile = user_manager.get_user_profile(session['username'])
        return render_template('profile_management.html', profile=user_profile)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8367, debug=False)
