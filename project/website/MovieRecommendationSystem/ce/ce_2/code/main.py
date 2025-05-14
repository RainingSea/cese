from flask import Flask, render_template, request, redirect, url_for, session
from movie_recommender import MovieRecommender

app = Flask(__name__)
app.secret_key = 'secret_key'
recommender = MovieRecommender()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if 'register' in request.form:
            if recommender.register_user(username, password):
                return redirect(url_for('login'))
            else:
                return render_template('login.html', error="Username already exists")
        else:
            if recommender.login_user(username, password):
                session['username'] = username
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    recommendations = recommender.get_recommendations(username)
    return render_template('home.html', movies=recommendations, username=username)

@app.route('/movie/<title>')
def movie(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    movie_details = recommender.get_movie_details(title)
    if not movie_details:
        return redirect(url_for('home'))
    
    return render_template('movie.html', movie=movie_details, username=session['username'])

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    movie_title = request.form['movie_title']
    recommender.add_favorite(username, movie_title)
    return redirect(url_for('movie', title=movie_title))

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    movie_title = request.form['movie_title']
    recommender.remove_favorite(username, movie_title)
    return redirect(url_for('favorites'))

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    favorites = recommender.get_favorites(username)
    movies = []
    for title in favorites:
        movie_details = recommender.get_movie_details(title)
        if movie_details:
            movies.append(movie_details)
    
    return render_template('favorites.html', movies=movies, username=username)

@app.route('/search', methods=['GET'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('query', '')
    results = recommender.search_movies(query)
    return render_template('search.html', movies=results, username=session['username'], query=query)

if __name__ == '__main__':
    app.run(port=8004, debug=False)
