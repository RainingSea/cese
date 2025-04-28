from flask import Flask, render_template, request, redirect, session, url_for
from user_manager import UserManager
from resource_manager import ResourceManager
from message_manager import MessageManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
resource_manager = ResourceManager('resources.txt')
message_manager = MessageManager('messages.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        interests = request.form['interests']
        user_manager.update_profile(session['username'], interests)
    return render_template('profile.html', user=session['username'])

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        resource_manager.share_resource(title, link)
    resources = resource_manager.get_resources()
    return render_template('resources.html', resources=resources)

@app.route('/resources/<int:resource_id>')
def resource_details(resource_id):
    resources = resource_manager.get_resources()
    if 0 <= resource_id < len(resources):
        resource = resources[resource_id]
        return render_template('resource_details.html', resource=resource)
    return redirect(url_for('resources'))

@app.route('/messaging', methods=['GET', 'POST'])
def messaging():
    if request.method == 'POST':
        sender = session['username']
        receiver = request.form['receiver']
        content = request.form['content']
        message_manager.send_message(sender, receiver, content)
    messages = message_manager.get_messages(session['username'])
    return render_template('messaging.html', messages=messages)

@app.route('/study_groups')
def study_groups():
    return render_template('study_groups.html')

@app.route('/study_groups/messaging', methods=['GET', 'POST'])
def study_group_messaging():
    if request.method == 'POST':
        sender = session['username']
        receiver = request.form['receiver']
        content = request.form['content']
        message_manager.send_message(sender, receiver, content)
    messages = message_manager.get_messages(session['username'])
    return render_template('study_group_messaging.html', messages=messages)

if __name__ == '__main__':
    app.run(port=8417, debug=False)
