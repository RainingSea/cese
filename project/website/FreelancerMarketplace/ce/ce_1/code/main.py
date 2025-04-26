from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from freelancer_manager import FreelancerManager
from project_manager import ProjectManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
freelancer_manager = FreelancerManager()
project_manager = ProjectManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=8168, debug=False)
