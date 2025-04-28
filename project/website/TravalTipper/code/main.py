from flask import Flask, render_template, request, redirect, session, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> dict:
        users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def save_users(self) -> None:
        with open(self.users_file, 'w') as f:
            for username, password in self.users.items():
                f.write(f"{username}|{password}\n")

class TravelTipGenerator:
    def __init__(self, tips_file: str):
        self.tips_file = tips_file
        self.tips = self.load_tips()

    def generate_tips(self, destination: str, interests: list) -> list:
        filtered_tips = []
        for tip in self.tips:
            if destination.lower() in tip[0].lower() and any(interest.lower() in tip[1].lower() for interest in interests):
                filtered_tips.append(tip)
        return filtered_tips

    def load_tips(self) -> list:
        tips = []
        if os.path.exists(self.tips_file):
            with open(self.tips_file, 'r') as f:
                for line in f:
                    destination, tip = line.strip().split('|')
                    tips.append((destination, tip))
        return tips

class FavoritesManager:
    def __init__(self, favorites_file: str):
        self.favorites_file = favorites_file

    def save_favorite(self, username: str, tip: str) -> bool:
        with open(self.favorites_file, 'a') as f:
            f.write(f"{username}|{tip}\n")
        return True

    def load_favorites(self, username: str) -> list:
        favorites = []
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, 'r') as f:
                for line in f:
                    user, tip = line.strip().split('|')
                    if user == username:
                        favorites.append(tip)
        return favorites

user_manager = UserManager('users.txt')
travel_tip_generator = TravelTipGenerator('travel_tips.txt')
favorites_manager = FavoritesManager('favorites.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        flash('Username already taken', 'danger')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    tips = []
    if request.method == 'POST':
        destination = request.form['destination']
        interests = request.form['interests'].split(',')
        tips = travel_tip_generator.generate_tips(destination, interests)
    
    favorites = favorites_manager.load_favorites(username)
    return render_template('dashboard.html', tips=tips, favorites=favorites)

@app.route('/save_favorite', methods=['POST'])
def save_favorite():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    tip = request.form['tip']
    favorites_manager.save_favorite(username, tip)
    flash('Tip saved to favorites!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8437, debug=False)
