from flask import Flask, render_template, request, redirect, session
from user import User
from feedback import Feedback

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class App:
    def __init__(self):
        self.users = User.load_all()
        self.feedbacks = Feedback.load_all()

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def submit_feedback(self, user: str, category: str, content: str) -> None:
        new_feedback = Feedback(user, category, content)
        new_feedback.save()
        self.feedbacks.append(new_feedback)

    def review_feedback(self) -> list:
        return self.feedbacks

    def get_feedback_status(self, user: str) -> list:
        return [feedback for feedback in self.feedbacks if feedback.user == user]

tracker = App()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.login(username, password):
            return redirect('/feedback')
    return render_template('login.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        category = request.form['category']
        content = request.form['content']
        tracker.submit_feedback(session['username'], category, content)
        return redirect('/status')
    return render_template('feedback.html')

@app.route('/review')
def review():
    return render_template('review.html', feedbacks=tracker.review_feedback())

@app.route('/status')
def status():
    user_feedbacks = tracker.get_feedback_status(session.get('username', ''))
    return render_template('status.html', feedbacks=user_feedbacks)

if __name__ == '__main__':
    app.run(port=8658, debug=False)
