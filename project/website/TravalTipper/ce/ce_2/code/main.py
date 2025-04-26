from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class TravelTipManager:
    def __init__(self):
        self.tips = {}
        self.load_tips()

    def load_tips(self) -> None:
        try:
            with open('travel_tips.txt', 'r') as file:
                for line in file:
                    destination, interest, tip = line.strip().split('|')
                    if destination not in self.tips:
                        self.tips[destination] = []
                    self.tips[destination].append((interest, tip))
        except FileNotFoundError:
            pass

    def get_recommendations(self, destination: str, interests: list) -> list:
        recommendations = []
        if destination in self.tips:
            for interest in interests:
                for tip in self.tips[destination]:
                    if tip[0] == interest:
                        recommendations.append(tip[1])
        return recommendations

    def save_favorite(self, user: str, tip: str) -> None:
        with open('favorites.txt', 'a') as file:
            file.write(f"{user}|{tip}\n")

user_manager = UserManager()
travel_tip_manager = TravelTipManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('travel_details'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/travel_details', methods=['GET', 'POST'])
def travel_details():
    if request.method == 'POST':
        destination = request.form['destination']
        duration = request.form['duration']
        interests = request.form.getlist('interests')
        recommendations = travel_tip_manager.get_recommendations(destination, interests)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('travel_details.html')

@app.route('/favorites', methods=['GET'])
def favorites():
    user = session.get('username')
    favorites = []
    try:
        with open('favorites.txt', 'r') as file:
            for line in file:
                f_user, tip = line.strip().split('|')
                if f_user == user:
                    favorites.append(tip)
    except FileNotFoundError:
        pass
    return render_template('favorites.html', favorites=favorites)

if __name__ == '__main__':
    app.run(port=8264, debug=False)
