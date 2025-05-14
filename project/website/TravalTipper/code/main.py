from flask import Flask, render_template, request, redirect, url_for, session, flash
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
        username = request.form.get('username')
        password = request.form.get('password')
        
        if tipper.login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        result = tipper.register_user(username, password)
        if result == "SUCCESS":
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        elif result == "USER_EXISTS":
            flash('Username already taken', 'error')
        elif result == "EMPTY_FIELDS":
            flash('Username and password cannot be empty', 'error')
        else:
            flash('Registration failed', 'error')
    
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
        destination = request.form.get('destination')
        interests = request.form.getlist('interests')
        
        tips = tipper.get_tips(destination, interests)
        return render_template('tips.html', tips=tips, search_query='', destination=destination, interests=interests)
    
    return render_template('tips.html', tips=[], search_query='')

@app.route('/search', methods=['GET'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('query', '')
    tips = tipper.search_tips(query) if query else []
    return render_template('tips.html', tips=tips, search_query=query)

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    favorites = tipper.get_favorites(session['username'])
    return render_template('favorites.html', favorites=favorites)

@app.route('/save_favorite/<tip_id>')
def save_favorite(tip_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    result = tipper.save_favorite(session['username'], tip_id)
    if result == "SUCCESS":
        flash('Tip saved to favorites!', 'success')
    elif result == "ALREADY_FAVORITED":
        flash('This tip is already in your favorites', 'info')
    else:
        flash('Failed to save favorite', 'error')
    
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))