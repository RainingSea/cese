from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.users_file = 'users.txt'
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def validate_login(self, username, password):
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
    def __init__(self):
        self.tips_file = 'tips.txt'
        if not os.path.exists(self.tips_file):
            with open(self.tips_file, 'w') as f:
                f.write("1:2023-01-01:Drink at least 8 glasses of water daily\n")
                f.write("2:2023-01-02:Get 7-8 hours of sleep each night\n")
                f.write("3:2023-01-03:Exercise for 30 minutes daily\n")

    def get_current_tip(self):
        with open(self.tips_file, 'r') as f:
            lines = f.readlines()
            if lines:
                return lines[-1].strip().split(':')[2]
        return "No tips available"

    def get_all_tips(self):
        tips = []
        with open(self.tips_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 3:
                    tips.append({'id': parts[0], 'date': parts[1], 'content': parts[2]})
        return tips

    def search_tips(self, query):
        results = []
        with open(self.tips_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 3 and query.lower() in parts[2].lower():
                    results.append({'id': parts[0], 'date': parts[1], 'content': parts[2]})
        return results

class FeedbackManager:
    def __init__(self):
        self.feedback_file = 'feedback.txt'
        if not os.path.exists(self.feedback_file):
            open(self.feedback_file, 'w').close()

    def submit_feedback(self, username, tip_id, rating, comment):
        with open(self.feedback_file, 'a') as f:
            f.write(f"{username}:{tip_id}:{rating}:{comment}\n")
        return True

user_manager = UserManager()
tip_manager = TipManager()
feedback_manager = FeedbackManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    if user_manager.validate_login(username, password):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    if user_manager.register_user(username, password, email):
        return redirect(url_for('login'))
    return redirect(url_for('register'))

@app.route('/dashboard')
def dashboard():
    current_tip = tip_manager.get_current_tip()
    return render_template('dashboard.html', tip=current_tip)

@app.route('/archive')
def archive():
    tips = tip_manager.get_all_tips()
    return render_template('archive.html', tips=tips)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = tip_manager.search_tips(query)
    return render_template('archive.html', tips=results)

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    username = request.form['username']
    tip_id = request.form['tip_id']
    rating = request.form['rating']
    comment = request.form['comment']
    
    feedback_manager.submit_feedback(username, tip_id, rating, comment)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8571, debug=False)
