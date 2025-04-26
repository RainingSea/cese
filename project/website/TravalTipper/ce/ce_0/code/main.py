from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from travel_tip_manager import TravelTipManager

app = Flask(__name__)

user_manager = UserManager()
travel_tip_manager = TravelTipManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('travel_input'))
        else:
            return "Login failed. Please check your credentials."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Username may already exist."
    return render_template('registration.html')

@app.route('/travel_input', methods=['GET', 'POST'])
def travel_input():
    if request.method == 'POST':
        destination = request.form['destination']
        tips = request.form['tips']
        travel_tip_manager.addTip(destination, tips)
        return redirect(url_for('travel_input'))
    return render_template('travel_input.html', tips=travel_tip_manager.getTips(""))

if __name__ == '__main__':
    app.run(port=8262, debug=False)
