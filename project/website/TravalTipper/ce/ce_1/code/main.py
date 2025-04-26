from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as file:
            users = {}
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
            return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username] == password:
            session['username'] = username
            return True
        return False

    def logout(self) -> None:
        session.pop('username', None)

class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        if not os.path.exists('tips.txt'):
            return []
        with open('tips.txt', 'r') as file:
            return [line.strip() for line in file]

    def generate_tips(self, destination: str, interests: list) -> list:
        # For simplicity, returning all tips that contain the destination
        return [tip for tip in self.tips if destination.lower() in tip.lower()]

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]

    def save_favorite(self, tip: str) -> None:
        with open('favorites.txt', 'a') as file:
            file.write(f"{tip}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager = UserManager()
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/travel', methods=['GET', 'POST'])
def travel_details():
    if request.method == 'POST':
        destination = request.form['destination']
        interests = request.form.getlist('interests')
        tip_manager = TipManager()
        tips = tip_manager.generate_tips(destination, interests)
        return render_template('recommendations.html', tips=tips)
    return render_template('travel_details.html')

@app.route('/logout')
def logout():
    user_manager = UserManager()
    user_manager.logout()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8263, debug=False)
