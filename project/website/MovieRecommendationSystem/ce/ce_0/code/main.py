import http.server
import socketserver
import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.movie_manager = MovieManager()

    def main(self):
        PORT = 8000
        handler = self.create_handler()
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"Serving at port {PORT}")
            httpd.serve_forever()

    def create_handler(self):
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(open('templates/login.html', 'rb').read())
                elif self.path == '/register':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(open('templates/register.html', 'rb').read())
                elif self.path == '/search':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(open('templates/search.html', 'rb').read())
                elif self.path == '/recommendations':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(open('templates/recommendations.html', 'rb').read())
                elif self.path == '/favorites':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(open('templates/favorites.html', 'rb').read())
                else:
                    self.send_error(404)

            def do_POST(self):
                if self.path == '/login':
                    self.handle_login()
                elif self.path == '/register':
                    self.handle_register()
                elif self.path == '/search':
                    self.handle_search()

            def handle_login(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                username, password = post_data.split('&')
                username = username.split('=')[1]
                password = password.split('=')[1]
                if self.server.main.user_manager.login(username, password):
                    self.send_response(302)
                    self.send_header('Location', '/recommendations')
                    self.end_headers()
                else:
                    self.send_response(401)
                    self.end_headers()

            def handle_register(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                username, password = post_data.split('&')
                username = username.split('=')[1]
                password = password.split('=')[1]
                if self.server.main.user_manager.register(username, password):
                    self.send_response(302)
                    self.send_header('Location', '/')
                    self.end_headers()
                else:
                    self.send_response(400)
                    self.end_headers()

            def handle_search(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                query = post_data.split('=')[1]
                results = self.server.main.movie_manager.search_movies(query)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(results).encode('utf-8'))

        return Handler

if __name__ == "__main__":
    main_app = Main()
    main_app.user_manager.load_users()
    main_app.movie_manager.load_movies()
    main_app.main()