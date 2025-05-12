from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self):
        if not self.is_username_taken():
            with open('users.txt', 'a') as f:
                f.write(f"{self.username}|{self.password}\n")
            return True
        return False

    def is_username_taken(self):
        if not os.path.exists('users.txt'):
            return False
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username:
                    return True
        return False

    def login(self):
        if not os.path.exists('users.txt'):
            return False
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username and user_data[1] == self.password:
                    return True
        return False

class Feedback:
    def __init__(self, employee, comments, category):
        self.employee = employee
        self.comments = comments
        self.category = category
        self.status = 'Pending'

    def submit(self):
        with open('feedback.txt', 'a') as f:
            f.write(f"{self.employee}|{self.comments}|{self.category}|{self.status}\n")

    def get_status(self):
        if not os.path.exists('feedback.txt'):
            return []
        with open('feedback.txt', 'r') as f:
            feedbacks = []
            for line in f:
                feedback_data = line.strip().split('|')
                if feedback_data[0] == self.employee:
                    feedbacks.append(feedback_data)
            return feedbacks

class Manager:
    def review_feedback(self):
        if not os.path.exists('feedback.txt'):
            return []
        with open('feedback.txt', 'r') as f:
            return [line.strip().split('|') for line in f]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login():
            session['username'] = username
            return redirect(url_for('feedback'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register():
            return redirect(url_for('login'))
        else:
            return "Username already taken"
    return render_template('register.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        comments = request.form['comments']
        category = request.form['category']
        employee = session['username']
        if comments and category:  # Validate input
            feedback = Feedback(employee, comments, category)
            feedback.submit()
            return redirect(url_for('status'))
        else:
            return "Please fill in all fields."
    return render_template('feedback.html')

@app.route('/status')
def status():
    employee = session['username']
    feedback = Feedback(employee, '', '')
    feedbacks = feedback.get_status()
    return render_template('status.html', feedbacks=feedbacks)

@app.route('/review')
def review():
    manager = Manager()
    feedbacks = manager.review_feedback()
    return render_template('review.html', feedbacks=feedbacks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8500, debug=False)
