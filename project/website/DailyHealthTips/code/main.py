from flask import Flask, render_template, request, redirect, session
from flask_session import Session

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.users[username] = password

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

class TipManager:
    def __init__(self, tips_file: str):
        self.tips_file = tips_file
        self.load_tips()

    def load_tips(self):
        self.tips = []
        with open(self.tips_file, 'r') as file:
            self.tips = [line.strip() for line in file]

    def get_current_tip(self, index: int) -> str:
        return self.tips[index] if 0 <= index < len(self.tips) else ""

    def get_previous_tip(self, current_index: int) -> str:
        return self.get_current_tip(current_index - 1)

    def get_next_tip(self, current_index: int) -> str:
        return self.get_current_tip(current_index + 1)

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]

class FeedbackManager:
    def __init__(self, feedback_file: str):
        self.feedback_file = feedback_file
        self.load_feedback()

    def load_feedback(self):
        self.feedback = []
        with open(self.feedback_file, 'r') as file:
            self.feedback = [line.strip() for line in file]

    def submit_feedback(self, feedback: str) -> bool:
        with open(self.feedback_file, 'a') as file:
            file.write(f"{feedback}\n")
        self.feedback.append(feedback)
        return True

    def get_all_feedback(self) -> list:
        return self.feedback

app = Flask(__name__)
app.secret_key = 'supersecretkey'
Session(app)

user_manager = UserManager('users.txt')
tip_manager = TipManager('tips.txt')
feedback_manager = FeedbackManager('feedback.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            session['current_index'] = 0  # Reset index on login
            return redirect('/tips')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = user_manager.register(username, password)
        if result:
            return redirect('/')
        else:
            return "Registration failed, username may already exist."
    return render_template('register.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    current_index = session.get('current_index', 0)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'next':
            current_index += 1
        elif action == 'previous':
            current_index -= 1
        session['current_index'] = current_index
    return render_template('tips.html', tip=tip_manager.get_current_tip(current_index), current_index=current_index)

@app.route('/archive', methods=['GET', 'POST'])
def archive():
    if request.method == 'POST':
        query = request.form['query']
        tips = tip_manager.search_tips(query)
        return render_template('archive.html', tips=tips)
    return render_template('archive.html', tips=tip_manager.tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect('/feedback')
    return render_template('feedback.html', feedback_list=feedback_manager.get_all_feedback())

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('current_index', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8318, debug=False)
