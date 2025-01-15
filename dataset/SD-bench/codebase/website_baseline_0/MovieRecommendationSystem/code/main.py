from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from movie_manager import MovieManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
user_manager = UserManager()
movie_manager = MovieManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    recommendations = movie_manager.get_recommendations([])
    return render_template('home.html', recommendations=recommendations)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/movie/<title>')
def movie_details(title):
    movie = movie_manager.get_movie_details(title)
    return render_template('movie_details.html', movie=movie)

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    favorites = movie_manager.load_favorites(session['username'])
    return render_template('favorites.html', favorites=favorites)

@app.route('/add_favorite/<title>')
def add_favorite(title):
    if 'username' in session:
        movie_manager.add_to_favorites(session['username'], title)
    return redirect(url_for('favorites'))

@app.route('/remove_favorite/<title>')
def remove_favorite(title):
    if 'username' in session:
        movie_manager.remove_from_favorites(session['username'], title)
    return redirect(url_for('favorites'))

if __name__ == '__main__':
    user_manager.load_users()
    movie_manager.load_movies()
    app.run(port=8539, debug=False)
