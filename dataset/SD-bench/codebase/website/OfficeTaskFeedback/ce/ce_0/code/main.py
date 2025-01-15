from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
data_folder = './'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open(os.path.join(data_folder, 'users.txt'), 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load():
        users = []
        if os.path.exists(os.path.join(data_folder, 'users.txt')):
            with open(os.path.join(data_folder, 'users.txt'), 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

class Feedback:
    def __init__(self, employee_username: str, category: str, comment: str):
        self.employee_username = employee_username
        self.category = category
        self.comment = comment
        self.status = 'Pending'

    def save(self):
        with open(os.path.join(data_folder, 'feedback.txt'), 'a') as f:
            f.write(f"{self.employee_username}|{self.category}|{self.comment}|{self.status}\n")

    @staticmethod
    def load():
        feedbacks = []
        if os.path.exists(os.path.join(data_folder, 'feedback.txt')):
            with open(os.path.join(data_folder, 'feedback.txt'), 'r') as f:
                for line in f:
                    employee_username, category, comment, status = line.strip().split('|')
                    feedbacks.append(Feedback(employee_username, category, comment))
                    feedbacks[-1].status = status
        return feedbacks

class FeedbackTracker:
    def __init__(self):
        self.users = User.load()
        self.feedbacks = Feedback.load()

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        user = next((user for user in self.users if user.username == username), None)
        if user and user.password == password:
            session['username'] = username
            return True
        return False

    def submit_feedback(self, employee_username: str, category: str, comment: str):
        new_feedback = Feedback(employee_username, category, comment)
        new_feedback.save()
        self.feedbacks.append(new_feedback)

    def review_feedback(self):
        return self.feedbacks

    def get_feedback_status(self, employee_username: str):
        return [feedback for feedback in self.feedbacks if feedback.employee_username == employee_username]

tracker = FeedbackTracker()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if tracker.login(username, password):
        return redirect(url_for('feedback_page'))
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.register(username, password):
            return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if request.method == 'POST':
        category = request.form['category']
        comment = request.form['comment']
        tracker.submit_feedback(session['username'], category, comment)
        return redirect(url_for('feedback_page'))
    return render_template('feedback.html')

@app.route('/review')
def review_page():
    feedbacks = tracker.review_feedback()
    return render_template('review.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(port=8657, debug=False)
