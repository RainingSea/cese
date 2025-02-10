from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from TipManager import TipManager

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
        if user_manager.register_user(username, password):
            return redirect(url_for('login'))
        return "Registration failed. Username already exists."
    return render_template('register.html')

@app.route('/tips', methods=['GET'])
def tips():
    current_tip = tip_manager.get_current_tip()
    return render_template('tips.html', current_tip=current_tip)

@app.route('/archive', methods=['GET'])
def archive():
    return render_template('archive.html', tips=tip_manager.tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        with open('feedback.txt', 'a') as file:
            file.write(f"{feedback_text}\n")
        return redirect(url_for('tips'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=8618, debug=False)
