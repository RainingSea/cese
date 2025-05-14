from flask import Flask, render_template, request, redirect, url_for, session, flash
from user_manager import UserManager
from trip_manager import TripManager

app = Flask(__name__)
app.secret_key = 'secret_key'

user_manager = UserManager()
trip_manager = TripManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('trip_input'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        success, message = user_manager.login(username, password)
        if success:
            session['username'] = username
            flash(message, 'success')
            return redirect(url_for('trip_input'))
        flash(message, 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        success, message = user_manager.register(username, password)
        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        flash(message, 'error')
    return render_template('register.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        start = request.form.get('start', '').strip()
        destination = request.form.get('destination', '').strip()
        date = request.form.get('date', '').strip()
        
        if not all([start, destination, date]):
            flash('All trip details must be provided', 'error')
            return render_template('trip_input.html')
            
        return redirect(url_for('results', start=start, destination=destination, date=date))
    return render_template('trip_input.html')

@app.route('/results')
def results():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    start = request.args.get('start', '').strip()
    destination = request.args.get('destination', '').strip()
    date = request.args.get('date', '').strip()
    
    if not all([start, destination, date]):
        flash('Invalid trip parameters', 'error')
        return redirect(url_for('trip_input'))
    
    options, message = trip_manager.get_options(start, destination)
    if not options:
        flash(message, 'error')
        return redirect(url_for('trip_input'))
        
    return render_template('results.html', 
                         start=start, 
                         destination=destination, 
                         date=date, 
                         options=options['all_options'],
                         cheapest=options['cheapest'],
                         fastest=options['fastest'])

@app.route('/save_trip', methods=['POST'])
def save_trip():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    start = request.form.get('start', '').strip()
    destination = request.form.get('destination', '').strip()
    date = request.form.get('date', '').strip()
    option = request.form.get('option', '').strip()
    
    success, message = trip_manager.save_trip(username, start, destination, date, option)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('saved_trips'))

@app.route('/saved_trips')
def saved_trips():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    trips, message = trip_manager.get_saved_trips(username)
    if not trips:
        flash(message, 'info')
    return render_template('saved_trips.html', trips=trips)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8078, debug=False)
