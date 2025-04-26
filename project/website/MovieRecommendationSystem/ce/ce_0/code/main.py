import http.server
import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.movie_manager = MovieManager()

    def main(self):
        self.load_data()
        server_address = ('', 8000)
        httpd = http.server.HTTPServer(server_address, self)
        print("Starting server on port 8000...")
        httpd.serve_forever()

    def load_data(self):
        self.user_manager.load_users()
        self.movie_manager.load_movies()
        self.movie_manager.load_favorites()

    def do_GET(self):
        if self.path == '/':
            self.handle_login()
        elif self.path == '/register':
            self.handle_register()
        elif self.path == '/recommendations':
            self.handle_recommendations()
        elif self.path.startswith('/search'):
            self.handle_search()
        elif self.path.startswith('/movie_details'):
            self.handle_movie_details()
        elif self.path == '/favorites':
            self.handle_favorites()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_login(self):
        with open('templates/login.html', 'r') as file:
            content = file.read()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content.encode())

    def handle_register(self):
        with open('templates/register.html', 'r') as file:
            content = file.read()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content.encode())

    def handle_recommendations(self):
        recommendations = self.movie_manager.get_recommendations({})
        with open('templates/recommendations.html', 'r') as file:
            content = file.read()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content.encode())

    def handle_search(self):
        query = self.path.split('=')[1]
        results = self.movie_manager.search_movies(query)
        with open('templates/search_results.html', 'r') as file:
            content = file.read()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content.encode())

    def handle_movie_details(self):
        title = self.path.split('=')[1]
        details = self.movie_manager.get_movie_details(title)
        with open('templates/movie_details.html', 'r') as file:
            content = file.read()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content.encode())

    def handle_favorites(self):
        favorites = self.movie_manager.get_favorites('username')  # Replace 'username' with actual session user
        with open('templates/favorites.html', 'r') as file:
            content = file.read()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content.encode())

if __name__ == '__main__':
    app = Main()
    app.main()