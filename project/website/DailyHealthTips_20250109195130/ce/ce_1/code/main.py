from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from TipManager import TipManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

user_manager = UserManager('users.txt')
tip_manager = TipManager('tips.txt', 'feedback.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/tip_display')
def tip_display():
    daily_tip = tip_manager.get_daily_tip()
    return render_template('tip_display.html', tip=daily_tip)

@app.route('/tips_archive')
def tips_archive():
    all_tips = tip_manager.get_all_tips()
    return render_template('tips_archive.html', tips=all_tips)

@app.route('/search_tips', methods=['GET', 'POST'])
def search_tips():
    if request.method == 'POST':
        query = request.form['query']
        results = tip_manager.search_tips(query)
        return render_template('tips_archive.html', tips=results)
    return redirect(url_for('tips_archive'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        tip_manager.submit_feedback(feedback_text)
        return redirect(url_for('tip_display'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=8356, debug=False)
