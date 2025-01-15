from flask import Flask, render_template, request, redirect, session
from user import User
from feedback import Feedback
from category import Category

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = User()
feedback_manager = Feedback()
category_manager = Category()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return render_template('registration.html', error="Username already exists.")
    return render_template('registration.html')

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        username = session.get('username')
        feedback_text = request.form['feedback_text']
        category = request.form['category']
        feedback_manager.submit_feedback(username, feedback_text, category)
        return redirect('/feedback_review')
    categories = category_manager.get_categories()
    return render_template('feedback_submission.html', categories=categories)

@app.route('/feedback_review')
def feedback_review():
    feedback_list = feedback_manager.review_feedback()
    return render_template('feedback_review.html', feedback_list=feedback_list)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/submit_feedback')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8542, debug=False)
