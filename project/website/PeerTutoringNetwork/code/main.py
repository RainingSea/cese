from flask import Flask, render_template, request, redirect, session, flash, url_for
from auth import AuthHandler
from tutor_manager import TutorHandler
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'dev_key'
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    auth_handler = AuthHandler('data/users.txt')
    tutor_handler = TutorHandler('data/tutors.txt', 'data/requests.txt')
    
    @app.route('/')
    def home():
        if 'username' in session:
            return redirect(url_for('dashboard'))
        return render_template('login.html', title='Login')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            if not username or not password:
                flash('Username and password are required')
                return render_template('login.html', title='Login')
            
            if auth_handler.login(username, password):
                session['username'] = username
                user = auth_handler.get_user(username)
                if user:
                    session['email'] = user['email']
                return redirect(url_for('dashboard'))
            flash('Invalid credentials')
        return render_template('login.html', title='Login')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            email = request.form.get('email', '').strip()
            
            if not all([username, password, email]):
                flash('All fields are required')
                return render_template('register.html', title='Register')
            
            if auth_handler.register(username, password, email):
                flash('Registration successful. Please login.')
                return redirect(url_for('login'))
            return render_template('register.html', title='Register')
        return render_template('register.html', title='Register')
    
    @app.route('/dashboard')
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('login'))
        return render_template('dashboard.html', 
                            title='Dashboard',
                            username=session['username'])
    
    @app.route('/tutors')
    def tutors():
        if 'username' not in session:
            return redirect(url_for('login'))
        tutors_list = tutor_handler.get_all_tutors()
        return render_template('tutors.html', 
                            title='Tutors',
                            tutors=tutors_list)
    
    @app.route('/request/<tutor_id>', methods=['GET', 'POST'])
    def request_tutor(tutor_id):
        if 'username' not in session:
            return redirect(url_for('login'))
        
        tutor = next((t for t in tutor_handler.get_all_tutors() if t['id'] == tutor_id), None)
        if not tutor:
            flash('Tutor not found')
            return redirect(url_for('tutors'))
            
        if request.method == 'POST':
            subject = request.form.get('subject', '').strip()
            details = request.form.get('details', '').strip()
            date = request.form.get('date', '').strip()
            
            if not all([subject, details, date]):
                flash('All fields are required')
                return render_template('request.html',
                                    title='Request Tutor',
                                    tutor_id=tutor_id,
                                    tutor_name=tutor['name'])
            
            if tutor_handler.add_request(session['username'], tutor_id, subject, details, date):
                flash('Request submitted successfully')
                return redirect(url_for('profile'))
            flash('Invalid date format. Use YYYY-MM-DD')
        
        return render_template('request.html', 
                            title='Request Tutor',
                            tutor_id=tutor_id,
                            tutor_name=tutor['name'])
    
    @app.route('/profile')
    def profile():
        if 'username' not in session:
            return redirect(url_for('login'))
        
        user = auth_handler.get_user(session['username'])
        requests = tutor_handler.get_requests(session['username'])
        return render_template('profile.html', 
                            title='Profile',
                            username=session['username'],
                            email=user.get('email', '') if user else '',
                            requests=requests)
    
    @app.route('/cancel_request/<request_id>')
    def cancel_request(request_id):
        if 'username' not in session:
            return redirect(url_for('login'))
        
        if tutor_handler.cancel_request(session['username'], request_id):
            flash('Request cancelled successfully')
        else:
            flash('Failed to cancel request')
        return redirect(url_for('profile'))
    
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message = request.form.get('message', '').strip()
            
            if not all([name, email, message]):
                flash('All fields are required')
            else:
                flash('Message sent successfully')
                return redirect(url_for('contact'))
        
        return render_template('contact.html', title='Contact Us')
    
    @app.route('/logout')
    def logout():
        session.pop('username', None)
        session.pop('email', None)
        return redirect(url_for('home'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8031, debug=False)
