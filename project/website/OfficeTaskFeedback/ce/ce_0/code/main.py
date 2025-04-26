from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

class FeedbackManager:
    def __init__(self):
        self.feedbacks = self.load_feedback()

    def load_feedback(self):
        if not os.path.exists('feedback.txt'):
            return []
        with open('feedback.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def submit_feedback(self, username: str, feedback: str, category: str) -> bool:
        self.feedbacks.append([username, feedback, category, 'Pending'])
        self.save_feedback()
        return True

    def save_feedback(self):
        with open('feedback.txt', 'w') as file:
            for feedback in self.feedbacks:
                file.write('|'.join(feedback) + '\n')

    def get_feedback_status(self, username: str):
        return [feedback for feedback in self.feedbacks if feedback[0] == username]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    feedback_manager = FeedbackManager()
    if request.method == 'POST':
        username = request.form['username']
        feedback_text = request.form['feedback']
        category = request.form['category']
        feedback_manager.submit_feedback(username, feedback_text, category)
        return redirect(url_for('status'))
    return render_template('feedback.html')

@app.route('/status')
def status():
    feedback_manager = FeedbackManager()
    username = request.args.get('username')
    feedbacks = feedback_manager.get_feedback_status(username)
    return render_template('status.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(port=8198, debug=False)
