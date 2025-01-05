from flask import Flask, render_template, request, redirect, session
from user import User
from story import Story
from auth import Auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth = Auth()

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.login(username, password):
            session['username'] = username
            return redirect('/story_creation')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth.register(username, password, email):
            return redirect('/')
    return render_template('registration.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation_page():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['username']
        story = Story(title, content, user_id)
        story.save()
        return redirect('/story_creation')
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8090, debug=False)
