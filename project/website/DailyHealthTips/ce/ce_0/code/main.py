from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
    
    def authenticate(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                    return True
        return False
    
    def register(self, username, password, email):
        with open(self.users_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.startswith(username + '|'):
                    return False
            f.write(f"{username}|{password}|{email}\n")
        return True

class TipManager:
    def __init__(self, tips_file='tips.txt'):
        self.tips_file = tips_file
        self.current_index = 0
        self.tips = self._load_tips()
    
    def _load_tips(self):
        tips = []
        with open(self.tips_file, 'r') as f:
            for line in f:
                date, content = line.strip().split('|', 1)
                tips.append({'date': date, 'content': content})
        return tips
    
    def get_current_tip(self):
        if not self.tips:
            return None
        return self.tips[self.current_index]
    
    def get_next_tip(self):
        if not self.tips:
            return None
        self.current_index = (self.current_index + 1) % len(self.tips)
        return self.tips[self.current_index]
    
    def get_previous_tip(self):
        if not self.tips:
            return None
        self.current_index = (self.current_index - 1) % len(self.tips)
        return self.tips[self.current_index]
    
    def get_all_tips(self):
        return self.tips
    
    def search_tips(self, query):
        return [tip for tip in self.tips if query.lower() in tip['content'].lower()]

class FeedbackManager:
    def __init__(self, feedback_file='feedback.txt'):
        self.feedback_file = feedback_file
    
    def submit_feedback(self, username, tip_date, feedback):
        with open(self.feedback_file, 'a') as f:
            f.write(f"{username}|{tip_date}|{feedback}\n")
        return True
    
    def get_feedback(self):
        feedbacks = []
        with open(self.feedback_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|', 2)
                if len(parts) == 3:
                    feedbacks.append({
                        'username': parts[0],
                        'tip_date': parts[1],
                        'feedback': parts[2]
                    })
        return feedbacks

user_manager = UserManager()
tip_manager = TipManager()
feedback_manager = FeedbackManager()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('main'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.authenticate(username, password):
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/main')
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    current_tip = tip_manager.get_current_tip()
    return render_template('main.html', tip=current_tip, username=session['username'])

@app.route('/next_tip')
def next_tip():
    if 'username' not in session:
        return redirect(url_for('login'))
    tip = tip_manager.get_next_tip()
    return render_template('main.html', tip=tip, username=session['username'])

@app.route('/previous_tip')
def previous_tip():
    if 'username' not in session:
        return redirect(url_for('login'))
    tip = tip_manager.get_previous_tip()
    return render_template('main.html', tip=tip, username=session['username'])

@app.route('/archive')
def archive():
    if 'username' not in session:
        return redirect(url_for('login'))
    search_query = request.args.get('search', '')
    if search_query:
        tips = tip_manager.search_tips(search_query)
    else:
        tips = tip_manager.get_all_tips()
    return render_template('archive.html', tips=tips, search_query=search_query)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        tip_date = request.form['tip_date']
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(session['username'], tip_date, feedback_text)
        return redirect(url_for('main'))
    
    current_tip = tip_manager.get_current_tip()
    return render_template('feedback.html', tip_date=current_tip['date'] if current_tip else '')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8570, debug=False)
