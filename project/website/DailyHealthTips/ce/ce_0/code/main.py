from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from tip_manager import TipManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
tip_manager = TipManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        return "Registration failed. Username already exists."
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    current_tip = tip_manager.get_current_tip()
    return render_template('tip.html', tip=current_tip)

@app.route('/archive', methods=['GET'])
def archive():
    if 'username' not in session:
        return redirect('/')
    return render_template('archive.html', tips=tip_manager.tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        tip_manager.submit_feedback(feedback_text)
        return redirect('/dashboard')
    return render_template('feedback.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return "Login failed. Check your username and password."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8617, debug=False)
