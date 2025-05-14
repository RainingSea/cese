from flask import Flask, render_template, request, redirect, url_for, session, flash
from UserManager import UserManager
from MovieManager import MovieManager
from FileHandler import FileHandler
import fcntl

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

file_handler = FileHandler()
user_manager = UserManager(file_handler)
movie_manager = MovieManager(file_handler)

@app.route('/')
def login_page():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html', title='Login')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash('Invalid credentials', 'error')
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='Register')
    
    username = request.form['username']
    password = request.form['password']
    
    if user_manager.register(username, password):
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login_page'))
    flash('Registration failed. Username may already exist.', 'error')
    return redirect(url_for('register'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    username = session['username']
    recommendations = movie_manager.get_recommendations(username)
    return render_template('dashboard.html', movies=recommendations, title='Dashboard')

@app.route('/search', methods=['GET'])
def search():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    query = request.args.get('query', '')
    results = movie_manager.search(query)
    return render_template('search.html', movies=results, query=query, title='Search Results')

@app.route('/movie/<movie_id>')
def movie_details(movie_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    movie = movie_manager.get_movie_details(movie_id)
    if not movie:
        flash('Movie not found', 'error')
        return redirect(url_for('dashboard'))
    return render_template('movie.html', movie=movie, title=movie.title)

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    username = session['username']
    favorites = movie_manager.get_favorites(username)
    return render_template('favorites.html', movies=favorites, title='Your Favorites')

@app.route('/add_favorite/<movie_id>')
def add_favorite(movie_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    username = session['username']
    if movie_manager.get_movie_details(movie_id):
        movie_manager.add_favorite(username, movie_id)
        flash('Added to favorites', 'success')
    else:
        flash('Movie not found', 'error')
    return redirect(url_for('movie_details', movie_id=movie_id))

@app.route('/remove_favorite/<movie_id>')
def remove_favorite(movie_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    username = session['username']
    if movie_manager.remove_favorite(username, movie_id):
        flash('Removed from favorites', 'success')
    else:
        flash('Failed to remove from favorites', 'error')
    return redirect(url_for('favorites'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(port=8005, debug=False)
