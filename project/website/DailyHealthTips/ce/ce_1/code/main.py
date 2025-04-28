from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.tip_manager = TipManager()
        self.feedback_manager = FeedbackManager()

    def main(self):
        app.run(port=8316, debug=False)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Main().user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/tips')
def tips():
    current_tip = Main().tip_manager.get_current_tip()
    return render_template('tips.html', tip=current_tip)

@app.route('/archive')
def archive():
    return render_template('archive.html', tips=Main().tip_manager.tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        Main().feedback_manager.submit_feedback(feedback_text)
        return redirect(url_for('tips'))
    return render_template('feedback.html')

if __name__ == '__main__':
    Main().main()