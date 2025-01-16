from flask import Flask, render_template, request, redirect, session, flash
import json
from user_manager import UserManager
from resource_manager import ResourceManager
from message_manager import MessageManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
resource_manager = ResourceManager()
message_manager = MessageManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register_user(username, password):
            flash('Registration successful! You can now log in.', 'success')
            return redirect('/')
        else:
            flash('Username already exists. Please choose a different one.', 'danger')
    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        resources = resource_manager.resources
        messages = message_manager.messages
        return render_template('profile.html', username=session['username'], resources=resources, messages=messages)
    return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login_user(username, password):
            session['username'] = username
            flash('Login successful! Welcome back.', 'success')
            return redirect('/profile')
        flash('Invalid username or password. Please try again.', 'danger')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect('/')

@app.route('/add_resource', methods=['POST'])
def add_resource():
    if 'username' in session:
        title = request.form['title']
        link = request.form['link']
        description = request.form['description']
        resource_manager.add_resource(title, link, description)
        flash('Resource added successfully!', 'success')
        return redirect('/profile')
    flash('You need to be logged in to add resources.', 'danger')
    return redirect('/')

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' in session:
        receiver = request.form['receiver']
        content = request.form['content']
        if user_manager.user_exists(receiver):
            message_manager.send_message(session['username'], receiver, content)
            flash('Message sent successfully!', 'success')
        else:
            flash('Receiver does not exist.', 'danger')
        return redirect('/profile')
    flash('You need to be logged in to send messages.', 'danger')
    return redirect('/')

@app.route('/resource/<int:resource_id>')
def view_resource(resource_id):
    if 'username' in session:
        resource = resource_manager.get_resource(resource_id)
        if resource:
            return render_template('resource_detail.html', resource=resource)
        flash('Resource not found.', 'danger')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8640, debug=False)
