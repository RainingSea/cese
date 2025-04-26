from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from trip_manager import TripManager

app = Flask(__name__)
user_manager = UserManager()
trip_manager = TripManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        username = request.form['username']
        starting_point = request.form['starting_point']
        destination = request.form['destination']
        date = request.form['date']
        trip_manager.input_trip(username, starting_point, destination, date)
        return redirect(url_for('results', username=username, starting_point=starting_point, destination=destination))
    return render_template('trip_input.html')

@app.route('/results')
def results():
    username = request.args.get('username')
    starting_point = request.args.get('starting_point')
    destination = request.args.get('destination')
    options = trip_manager.get_transportation_options(starting_point, destination)
    return render_template('results.html', options=options)

if __name__ == '__main__':
    app.run(port=8275, debug=False)
