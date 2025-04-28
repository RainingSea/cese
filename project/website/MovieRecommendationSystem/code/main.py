from flask import Flask, render_template, request, redirect, url_for, flash, session
from user_manager import UserManager
from movie_manager import MovieManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager()
movie_manager = MovieManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('recommendations'))  # Redirect to recommendations page
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/recommendations', methods=['GET'])
def recommendations():
    return render_template('recommendations.html')  # New recommendations page

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        movies = movie_manager.search_movies(query)  # Search for movies based on user input
        return render_template('search.html', movies=movies)  # Render search results
    return render_template('search.html', movies=[])  # Render initial search page HTML template

@app.route('/movie/<title>', methods=['GET', 'POST'])
def movie_detail(title):
    movie = movie_manager.get_movie_details(title)
    if request.method == 'POST':
        username = session.get('username')
        if username:
            movie_manager.add_to_favorites(username, title)
            flash(f'{title} added to favorites!')
        else:
            flash('You must be logged in to add favorites.')
    return render_template('movie_detail.html', movie=movie)

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    username = session.get('username')  # Get username from session
    favorites = movie_manager.load_favorites(username)
    if request.method == 'POST':
        movie_title = request.form['movie_title']
        movie_manager.remove_from_favorites(username, movie_title)
        flash(f'{movie_title} removed from favorites!')
        return redirect(url_for('favorites'))
    return render_template('favorites.html', favorites=favorites)

if __name__ == '__main__':
    user_manager.load_users()
    movie_manager.load_movies()
    app.run(port=8353, debug=False)
