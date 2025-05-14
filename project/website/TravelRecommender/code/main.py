from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class RecommendationEngine:
    def __init__(self, dest_file='destinations.txt'):
        self.dest_file = dest_file

    def _load_destinations(self):
        destinations = []
        if os.path.exists(self.dest_file):
            with open(self.dest_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        destinations.append({
                            'id': parts[0],
                            'name': parts[1],
                            'activities': parts[2].split(','),
                            'climate': parts[3],
                            'min_budget': int(parts[4]),
                            'max_budget': int(parts[5]),
                            'description': parts[6]
                        })
        return destinations

    def get_recommendations(self, prefs):
        destinations = self._load_destinations()
        if not prefs:
            return destinations
        
        budget = prefs.get('budget', 0)
        activities = prefs.get('activities', [])
        climate = prefs.get('climate', '')
        
        filtered = []
        for dest in destinations:
            budget_ok = dest['min_budget'] <= int(budget) <= dest['max_budget']
            climate_ok = not climate or dest['climate'] == climate
            activities_ok = not activities or any(act in dest['activities'] for act in activities)
            
            if budget_ok and climate_ok and activities_ok:
                filtered.append(dest)
        return filtered

    def get_destination_by_name(self, name):
        destinations = self._load_destinations()
        for dest in destinations:
            if dest['name'] == name:
                return dest
        return None

class UserManager:
    def __init__(self):
        self.users_file = 'users.txt'
        
    def _username_exists(self, username):
        if not os.path.exists(self.users_file):
            return False
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_user = line.strip().split('|')[0]
                if stored_user == username:
                    return True
        return False
    
    def register(self, username, password):
        if self._username_exists(username):
            return False, 'Username already exists'
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True, ''
    
    def login(self, username, password):
        if not os.path.exists(self.users_file):
            return False
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_user, stored_pass = line.strip().split('|')
                if stored_user == username and stored_pass == password:
                    return True
        return False

class PreferenceManager:
    def __init__(self):
        self.prefs_file = 'preferences.txt'
        
    def save_prefs(self, username, budget, activities, climate):
        lines = []
        if os.path.exists(self.prefs_file):
            with open(self.prefs_file, 'r') as f:
                for line in f:
                    if not line.startswith(username + '|'):
                        lines.append(line)
        
        with open(self.prefs_file, 'w') as f:
            f.writelines(lines)
            f.write(f"{username}|{budget}|{','.join(activities)}|{climate}\n")
        return True
        
    def get_prefs(self, username):
        if not os.path.exists(self.prefs_file):
            return None
        with open(self.prefs_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    return {
                        'budget': parts[1],
                        'activities': parts[2].split(','),
                        'climate': parts[3]
                    }
        return None

class FavoritesManager:
    def __init__(self):
        self.favs_file = 'favorites.txt'
        
    def add_favorite(self, username, destination):
        with open(self.favs_file, 'a') as f:
            f.write(f"{username}|{destination}\n")
        return True
        
    def get_favorites(self, username):
        if not os.path.exists(self.favs_file):
            return []
        favorites = []
        with open(self.favs_file, 'r') as f:
            for line in f:
                user, dest = line.strip().split('|')
                if user == username:
                    favorites.append(dest)
        return favorites
        
    def remove_favorite(self, username, destination):
        if not os.path.exists(self.favs_file):
            return False
        lines = []
        removed = False
        with open(self.favs_file, 'r') as f:
            for line in f:
                user, dest = line.strip().split('|')
                if user == username and dest == destination:
                    removed = True
                else:
                    lines.append(line)
        if removed:
            with open(self.favs_file, 'w') as f:
                f.writelines(lines)
        return removed

recommendation_engine = RecommendationEngine()
user_manager = UserManager()
pref_manager = PreferenceManager()
fav_manager = FavoritesManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('preferences'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('preferences'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message = user_manager.register(username, password)
        if success:
            session['username'] = username
            return redirect(url_for('preferences'))
        return render_template('register.html', error=message)
    return render_template('register.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        budget = request.form['budget']
        activities = request.form.getlist('activities')
        climate = request.form['climate']
        pref_manager.save_prefs(session['username'], budget, activities, climate)
        return redirect(url_for('recommendations'))
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    if 'username' not in session:
        return redirect(url_for('login'))
    prefs = pref_manager.get_prefs(session['username'])
    recs = recommendation_engine.get_recommendations(prefs)
    favs = fav_manager.get_favorites(session['username'])
    return render_template('recommendations.html', recommendations=recs, favorites=favs)

@app.route('/details/<name>')
def destination_details(name):
    if 'username' not in session:
        return redirect(url_for('login'))
    destination = recommendation_engine.get_destination_by_name(name)
    if not destination:
        return redirect(url_for('recommendations'))
    return render_template('details.html', destination=destination)

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    favs = fav_manager.get_favorites(session['username'])
    destinations = []
    for fav in favs:
        dest = recommendation_engine.get_destination_by_name(fav)
        if dest:
            destinations.append(dest)
    return render_template('favorites.html', favorites=destinations)

@app.route('/add_favorite/<destination>')
def add_favorite(destination):
    if 'username' not in session:
        return redirect(url_for('login'))
    if recommendation_engine.get_destination_by_name(destination):
        fav_manager.add_favorite(session['username'], destination)
    return redirect(url_for('recommendations'))

@app.route('/remove_favorite/<destination>')
def remove_favorite(destination):
    if 'username' not in session:
        return redirect(url_for('login'))
    fav_manager.remove_favorite(session['username'], destination)
    return redirect(url_for('favorites'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8074, debug=False)
