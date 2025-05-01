from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def validate_user(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                    return True
        return False

    def register_user(self, username, password, email):
        if not username or not password or not email:
            return False
            
        with open(self.users_file, 'a') as f:
            f.write(f"{username}:{password}:{email}\n")
        return True

class TipManager:
    def __init__(self, tips_file='tips.txt'):
        self.tips_file = tips_file
        if not os.path.exists(self.tips_file):
            open(self.tips_file, 'w').close()
        self.tips = self._load_tips()
        self.current_index = len(self.tips) - 1 if self.tips else -1

    def _load_tips(self):
        tips = []
        with open(self.tips_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 3:
                    tips.append({
                        'date': parts[0],
                        'title': parts[1],
                        'content': ':'.join(parts[2:])
                    })
        return tips

    def get_current_tip(self):
        if 0 <= self.current_index < len(self.tips):
            return self.tips[self.current_index]
        return None

    def get_next_tip(self):
        if self.current_index < len(self.tips) - 1:
            self.current_index += 1
        return self.get_current_tip()

    def get_previous_tip(self):
        if self.current_index > 0:
            self.current_index -= 1
        return self.get_current_tip()

    def get_all_tips(self):
        return self.tips

    def search_tips(self, query):
        return [tip for tip in self.tips 
                if query.lower() in tip['title'].lower() 
                or query.lower() in tip['content'].lower()]

class FeedbackManager:
    def __init__(self, feedback_file='feedback.txt'):
        self.feedback_file = feedback_file
        if not os.path.exists(self.feedback_file):
            open(self.feedback_file, 'w').close()

    def submit_feedback(self, username, feedback):
        if not username or not feedback:
            return False
            
        date = datetime.now().strftime('%Y-%m-%d')
        with open(self.feedback_file, 'a') as f:
            f.write(f"{username}:{date}:{feedback}\n")
        return True

    def get_all_feedback(self):
        feedbacks = []
        with open(self.feedback_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 3:
                    feedbacks.append({
                        'username': parts[0],
                        'date': parts[1],
                        'feedback': ':'.join(parts[2:])
                    })
        return feedbacks

user_manager = UserManager()
tip_manager = TipManager()
feedback_manager = FeedbackManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register_user(username, password, email):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Registration failed")
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    action = request.args.get('action')
    if action == 'next':
        tip = tip_manager.get_next_tip()
    elif action == 'prev':
        tip = tip_manager.get_previous_tip()
    else:
        tip = tip_manager.get_current_tip()
    
    return render_template('dashboard.html', tip=tip, username=session['username'])

@app.route('/archive')
def archive():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('query')
    if query:
        tips = tip_manager.search_tips(query)
    else:
        tips = tip_manager.get_all_tips()
    
    return render_template('archive.html', tips=tips, username=session['username'])

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        feedback = request.form['feedback']
        if feedback_manager.submit_feedback(session['username'], feedback):
            return redirect(url_for('dashboard'))
        else:
            return render_template('feedback.html', error="Feedback submission failed")
    return render_template('feedback.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8572, debug=False)
