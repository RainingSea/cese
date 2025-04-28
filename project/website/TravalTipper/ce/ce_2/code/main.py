from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_user_data()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def save_user_data(self):
        with open(self.users_file, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class TipGenerator:
    def __init__(self, tips_file):
        self.tips_file = tips_file
        self.tips = self.load_tips()

    def load_tips(self):
        tips = []
        try:
            with open(self.tips_file, 'r') as file:
                for line in file:
                    tips.append(line.strip())
        except FileNotFoundError:
            pass
        return tips

    def generate_tips(self, destination: str, duration: str, interests: list) -> list:
        # For simplicity, returning a static list of tips.
        return [f"Tip for {destination} with duration {duration} and interests {', '.join(interests)}"]

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]

    def save_favorite_tips(self, tip: str):
        with open('favorite_tips.txt', 'a') as file:
            file.write(f"{tip}\n")

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager('users.txt')
tip_generator = TipGenerator('travel_tips.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('travel_details'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists. Please choose another."
    return render_template('register.html')

@app.route('/travel_details', methods=['GET', 'POST'])
def travel_details():
    if request.method == 'POST':
        destination = request.form['destination']
        duration = request.form['duration']
        interests = request.form.getlist('interests')
        tips = tip_generator.generate_tips(destination, duration, interests)
        return render_template('travel_details.html', tips=tips)
    return render_template('travel_details.html', tips=[])

if __name__ == '__main__':
    app.run(port=8436, debug=False)
