from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class TravelRecommender:
    def __init__(self):
        self.users_file = 'users.txt'
        self.prefs_file = 'preferences.txt'
        self.dests_file = 'destinations.txt'
        self.favs_file = 'favorites.txt'

    def register_user(self, username, password):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login_user(self, username, password):
        if not os.path.exists(self.users_file):
            return False
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_user, stored_pass = line.strip().split('|')
                if stored_user == username and stored_pass == password:
                    return True
        return False

    def save_preferences(self, username, budget, activities, climate):
        prefs = []
        if os.path.exists(self.prefs_file):
            with open(self.prefs_file, 'r') as f:
                prefs = [line.strip() for line in f if not line.startswith(username)]
        
        pref_line = f"{username}|{budget}|{','.join(activities)}|{climate}"
        prefs.append(pref_line)
        
        with open(self.prefs_file, 'w') as f:
            f.write('\n'.join(prefs))

    def get_recommendations(self, username):
        if not os.path.exists(self.prefs_file) or not os.path.exists(self.dests_file):
            return []
        
        user_prefs = None
        with open(self.prefs_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    user_prefs = {
                        'budget': int(parts[1]),
                        'activities': parts[2].split(','),
                        'climate': parts[3]
                    }
                    break
        
        if not user_prefs:
            return []
        
        recommendations = []
        with open(self.dests_file, 'r') as f:
            for line in f:
                name, activities, climate, cost = line.strip().split('|')
                cost = int(cost)
                if (cost <= user_prefs['budget'] and 
                    any(act in user_prefs['activities'] for act in activities.split(',')) and 
                    climate == user_prefs['climate']):
                    recommendations.append({
                        'name': name,
                        'activities': activities,
                        'climate': climate,
                        'cost': cost
                    })
        return recommendations

    def get_destination_details(self, name):
        if not os.path.exists(self.dests_file):
            return None
        with open(self.dests_file, 'r') as f:
            for line in f:
                dest_name, activities, climate, cost = line.strip().split('|')
                if dest_name == name:
                    return {
                        'name': dest_name,
                        'activities': activities,
                        'climate': climate,
                        'cost': cost
                    }
        return None

    def save_favorite(self, username, destination):
        with open(self.favs_file, 'a') as f:
            f.write(f"{username}|{destination}\n")

recommender = TravelRecommender()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('recommendations'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if recommender.login_user(username, password):
            session['username'] = username
            return redirect(url_for('recommendations'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            return render_template('register.html', error='Username and password required')
        recommender.register_user(username, password)
        session['username'] = username
        return redirect(url_for('preferences'))
    return render_template('register.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        budget = request.form['budget']
        activities = request.form.getlist('activities')
        climate = request.form['climate']
        recommender.save_preferences(session['username'], budget, activities, climate)
        return redirect(url_for('recommendations'))
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    if 'username' not in session:
        return redirect(url_for('login'))
    recs = recommender.get_recommendations(session['username'])
    return render_template('recommendations.html', recommendations=recs)

@app.route('/details/<name>')
def details(name):
    if 'username' not in session:
        return redirect(url_for('login'))
    destination = recommender.get_destination_details(name)
    if not destination:
        return redirect(url_for('recommendations'))
    return render_template('details.html', destination=destination)

@app.route('/save_favorite/<name>')
def save_favorite(name):
    if 'username' not in session:
        return redirect(url_for('login'))
    recommender.save_favorite(session['username'], name)
    return redirect(url_for('details', name=name))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8072, debug=False)
