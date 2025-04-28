from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from travel_tip_generator import TravelTipGenerator
from favorites_manager import FavoritesManager

app = Flask(__name__)

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.travel_tip_generator = TravelTipGenerator()
        self.favorites_manager = FavoritesManager()
        self.user_manager.load_user_data()
        self.travel_tip_generator.load_tips()
        self.favorites_manager.load_favorites()

    def main(self):
        app.run(port=8434, debug=False)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Main().user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/travel_details', methods=['GET', 'POST'])
def travel_details():
    if request.method == 'POST':
        destination = request.form['destination']
        duration = request.form['duration']
        interests = request.form.getlist('interests')
        tips = Main().travel_tip_generator.generate_tips(destination, interests)
        return render_template('recommendations.html', tips=tips)
    return render_template('travel_details.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html', favorites=Main().favorites_manager.favorites)

if __name__ == '__main__':
    main_instance = Main()
    main_instance.main()