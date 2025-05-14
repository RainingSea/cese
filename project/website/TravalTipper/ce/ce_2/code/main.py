from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class TravelTipper:
    def __init__(self):
        self.user_file = 'users.txt'
        self.tips_file = 'tips.txt'
        self.favorites_file = 'favorites.txt'
        self._ensure_files_exist()
        
    def _ensure_files_exist(self):
        for file in [self.user_file, self.tips_file, self.favorites_file]:
            if not os.path.exists(file):
                open(file, 'w').close()
    
    def register_user(self, username, password):
        with open(self.user_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.split('|')[0] == username:
                    return False
            f.write(f"{username}|{password}\n")
        return True
    
    def login_user(self, username, password):
        with open(self.user_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False
    
    def get_tips(self, destination=None, interests=None):
        tips = []
        with open(self.tips_file, 'r') as f:
            for line in f:
                tip_dest, category, content = line.strip().split('|')
                if (not destination or destination.lower() in tip_dest.lower()) and \
                   (not interests or any(i.lower() in category.lower() for i in interests)):
                    tips.append({'destination': tip_dest, 'category': category, 'content': content})
        return tips
    
    def save_favorite(self, username, tip):
        with open(self.favorites_file, 'a') as f:
            f.write(f"{username}|{tip['destination']}|{tip['content']}\n")
        return True
    
    def get_favorites(self, username):
        favorites = []
        with open(self.favorites_file, 'r') as f:
            for line in f:
                user, dest, content = line.strip().split('|')
                if user == username:
                    favorites.append({'destination': dest, 'content': content})
        return favorites
    
    def remove_favorite(self, username, destination, content):
        lines = []
        removed = False
        with open(self.favorites_file, 'r') as f:
            lines = f.readlines()
        
        with open(self.favorites_file, 'w') as f:
            for line in lines:
                parts = line.strip().split('|')
                if not (parts[0] == username and parts[1] == destination and parts[2] == content):
                    f.write(line)
                else:
                    removed = True
        return removed

travel_tipper = TravelTipper()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if travel_tipper.login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if travel_tipper.register_user(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        destination = request.form.get('destination', '')
        interests = request.form.get('interests', '')
        interests_list = [i.strip() for i in interests.split(',')] if interests else []
        tips = travel_tipper.get_tips(destination, interests_list)
        return render_template('tips.html', tips=tips, username=session['username'])
    
    search_query = request.args.get('search', '')
    if search_query:
        tips = [tip for tip in travel_tipper.get_tips() 
               if search_query.lower() in tip['content'].lower() or 
                  search_query.lower() in tip['destination'].lower()]
    else:
        tips = travel_tipper.get_tips()
    
    return render_template('tips.html', tips=tips, username=session['username'])

@app.route('/save_favorite', methods=['POST'])
def save_favorite():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    tip = {
        'destination': request.form['destination'],
        'content': request.form['content']
    }
    travel_tipper.save_favorite(session['username'], tip)
    return redirect(url_for('tips'))

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    favorites = travel_tipper.get_favorites(session['username'])
    return render_template('favorites.html', favorites=favorites, username=session['username'])

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    destination = request.form['destination']
    content = request.form['content']
    travel_tipper.remove_favorite(session['username'], destination, content)
    return redirect(url_for('favorites'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8066, debug=False)
