from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from user_manager import UserManager
from tip_generator import TipGenerator

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager()
tip_generator = TipGenerator()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/main')
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return "Registration failed. Username may already exist."
    return render_template('registration.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        destination = request.form['destination']
        interests = request.form.getlist('interests')
        tips = tip_generator.generate_tips(destination, interests)
        return render_template('main.html', tips=tips)
    return render_template('main.html', tips=None)

if __name__ == '__main__':
    user_manager.load_users()
    tip_generator.load_tips()
    app.run(port=8435, debug=False)
