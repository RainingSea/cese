from flask import Flask, render_template, request, redirect, url_for, flash
from user import User
from story import Story
from auth import Auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        auth = Auth()
        if auth.register(username, password, email):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.')
    return render_template('register.html')

@app.route('/story', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        story = Story(username, title, content)
        story.save()
        flash('Story saved successfully!')
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8530, debug=False)
