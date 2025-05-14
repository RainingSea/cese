from flask import Flask, render_template, request, redirect, url_for, session
from travel_tipper import TravelTipper

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
tipper = TravelTipper()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tipper.login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tipper.register_user(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    favorites = tipper.get_favorites(session['username'])
    return render_template('dashboard.html', username=session['username'], favorites=favorites)

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        destination = request.form['destination']
        interests = request.form.getlist('interests')
        tips = tipper.get_tips(destination, interests)
        return render_template('tips.html', tips=tips, username=session['username'])
    
    return render_template('tips.html')

@app.route('/save_favorite', methods=['POST'])
def save_favorite():
    if 'username' not in session:
        return redirect(url_for('login'))
    tip_id = request.form['tip_id']
    tipper.save_favorite(session['username'], tip_id)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8064, debug=False)
