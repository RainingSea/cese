from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self) -> None:
        """Load users from the specified file."""
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        """Register a new user if the username is not taken."""
        if username in self.users:
            return False
        self.users[username] = password
        self.save_user_data()
        return True

    def login(self, username: str, password: str) -> bool:
        """Check if the username and password match."""
        if username in self.users and self.users[username] == password:
            return True
        return False

    def save_user_data(self) -> None:
        """Save user data to the specified file."""
        with open(self.users_file, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class TravelTipManager:
    def __init__(self, tips_file: str):
        self.tips_file = tips_file
        self.load_tips()

    def load_tips(self) -> None:
        """Load travel tips from the specified file."""
        self.tips = []
        try:
            with open(self.tips_file, 'r') as file:
                for line in file:
                    self.tips.append(line.strip())
        except FileNotFoundError:
            pass

    def get_tips(self, destination: str, interests: list) -> list:
        """Get tips based on destination and interests."""
        recommendations = []
        if destination:
            for interest in interests:
                for tip in self.tips:
                    if interest in tip or destination in tip:
                        recommendations.append(tip)
        return recommendations

    def search_tips(self, query: str) -> list:
        """Search for tips that match the query."""
        return [tip for tip in self.tips if query in tip]

user_manager = UserManager('users.txt')
travel_tip_manager = TravelTipManager('travel_tips.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('travel_details'))
        else:
            flash("Login Failed: Invalid username or password.")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Registration Failed: Username already taken.")
            return redirect(url_for('register'))
    return render_template('registration.html')

@app.route('/travel_details', methods=['GET', 'POST'])
def travel_details():
    """Handle travel details submission and recommendations display."""
    if request.method == 'POST':
        destination = request.form['destination']
        duration = request.form['duration']
        interests = request.form.getlist('interests')
        tips = travel_tip_manager.get_tips(destination, interests)
        return render_template('recommendations.html', tips=tips)
    return render_template('travel_details.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8265, debug=False)
