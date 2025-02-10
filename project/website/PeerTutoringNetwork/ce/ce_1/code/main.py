from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tutoring_request import TutoringRequest
from contact_message import ContactMessage
from peer_tutoring_network import PeerTutoringNetwork

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the Peer Tutoring Network
network = PeerTutoringNetwork()
network.load_users()
network.load_tutoring_requests()
network.load_contact_messages()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        network.register_user(username, password, email)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if network.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        user = network.get_user(session['username'])
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        network.contact_support(name, email, message)
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8719, debug=False)
