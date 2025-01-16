from flask import Flask, request, render_template, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None


class TravelTip:
    def __init__(self, destination: str, customs: str, safety_tips: str, transportation: str, etiquette: str, attractions: str):
        self.destination = destination
        self.customs = customs
        self.safety_tips = safety_tips
        self.transportation = transportation
        self.etiquette = etiquette
        self.attractions = attractions

    def save(self):
        with open('travel_tips.txt', 'a') as f:
            f.write(f"{self.destination}|{self.customs}|{self.safety_tips}|{self.transportation}|{self.etiquette}|{self.attractions}\n")

    @staticmethod
    def load(destination: str):
        with open('travel_tips.txt', 'r') as f:
            for line in f:
                tip_data = line.strip().split('|')
                if tip_data[0] == destination:
                    return TravelTip(*tip_data)
        return None


class Favorites:
    def __init__(self, user: str):
        self.user = user
        self.tips = []

    def add_tip(self, tip: TravelTip):
        self.tips.append(tip)

    def get_favorites(self):
        return self.tips


class TravelTipApp:
    def __init__(self):
        self.favorites = {}

    def register(self, username: str, password: str):
        user = User(username, password)
        user.save()

    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return True
        return False

    def input_travel_details(self, destination: str, duration: str, interests: str):
        # Placeholder for travel details input processing
        return []

    def generate_recommendations(self, details: dict):
        # Placeholder for generating recommendations based on travel details
        return []

    def search_tips(self, query: str):
        tips = []
        with open('travel_tips.txt', 'r') as f:
            for line in f:
                tip_data = line.strip().split('|')
                if query.lower() in tip_data[0].lower():
                    tips.append(TravelTip(*tip_data))
        return tips

    def save_favorite(self, tip: TravelTip):
        username = session.get('username')
        if username not in self.favorites:
            self.favorites[username] = Favorites(username)
        self.favorites[username].add_tip(tip)

    def logout(self):
        session.pop('username', None)


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance.register(username, password)
        return redirect(url_for('login_page'))
    return render_template('registration.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if app_instance.login(username, password):
        return redirect(url_for('travel_tips_page'))
    return redirect(url_for('login_page'))


@app.route('/travel_tips', methods=['GET', 'POST'])
def travel_tips_page():
    if request.method == 'POST':
        destination = request.form['destination']
        # Process travel details and generate recommendations
        return redirect(url_for('travel_tips_page'))
    return render_template('travel_tips.html')


if __name__ == '__main__':
    app_instance = TravelTipApp()
    app.run(port=8660, debug=False)
