from flask import Flask, render_template, request, redirect, url_for, session
from file_manager import FileManager, User, Tutor, TutoringRequest

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
file_manager = FileManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    users = file_manager.load_users()
    
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    
    return redirect(url_for('login'))  # Redirect back to login if authentication fails

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        file_manager.save_user(new_user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    tutors = file_manager.load_tutors()
    requests = file_manager.load_tutoring_requests()
    
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        request_tutoring = TutoringRequest(subject, details, preferred_date, session['username'])
        file_manager.save_tutoring_request(request_tutoring)
    
    return render_template('dashboard.html', tutors=tutors, requests=requests)

@app.route('/cancel_request', methods=['POST'])
def cancel_request():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    subject = request.form['subject']
    file_manager.cancel_tutoring_request(session['username'], subject)
    return redirect(url_for('dashboard'))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = next((u for u in file_manager.load_users() if u.username == session['username']), None)
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with open('contact_messages.txt', 'a') as f:
            f.write(f"{name}|{email}|{message}\n")
        return redirect(url_for('login'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8152, debug=True)
