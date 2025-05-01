from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from auth_manager import AuthManager
from tip_manager import TipManager
from feedback_manager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

auth_manager = AuthManager()
tip_manager = TipManager()
feedback_manager = FeedbackManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if auth_manager.authenticate(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if auth_manager.register_user(username, password):
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        flash('Username already exists or invalid input')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    current_tip = tip_manager.get_current_tip()
    all_tips = tip_manager.get_all_tips()
    current_tip_id = all_tips[0][0] if all_tips else None
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         current_tip=current_tip,
                         current_tip_id=current_tip_id)

@app.route('/tip/<action>/<current_tip_id>')
def navigate_tip(action, current_tip_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if action == 'next':
        tip = tip_manager.get_next_tip(current_tip_id)
    elif action == 'prev':
        tip = tip_manager.get_prev_tip(current_tip_id)
    else:
        return redirect(url_for('dashboard'))
    
    if tip:
        return render_template('dashboard.html', 
                            username=session['username'],
                            current_tip=tip[2],
                            current_tip_id=tip[0])
    return redirect(url_for('dashboard'))

@app.route('/api/tip/<action>/<current_tip_id>')
def api_navigate_tip(action, current_tip_id):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if action == 'next':
        tip = tip_manager.get_next_tip(current_tip_id)
    elif action == 'prev':
        tip = tip_manager.get_prev_tip(current_tip_id)
    else:
        return jsonify({'error': 'Invalid action'}), 400
    
    if tip:
        return jsonify({
            'tip_id': tip[0],
            'content': tip[2]
        })
    return jsonify({'error': 'No more tips'}), 404

@app.route('/archive')
def archive():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '')
    if search_query:
        tips = tip_manager.search_tips(search_query)
    else:
        tips = tip_manager.get_all_tips()
    return render_template('archive.html', tips=tips, search_query=search_query)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        tip_id = request.form.get('tip_id', '')
        comment = request.form.get('comment', '')
        if feedback_manager.submit_feedback(session['username'], tip_id, comment):
            flash('Thank you for your feedback!')
            return redirect(url_for('dashboard'))
        flash('Please fill all fields')
    
    all_tips = tip_manager.get_all_tips()
    return render_template('feedback.html', tips=all_tips)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8573, debug=False)
