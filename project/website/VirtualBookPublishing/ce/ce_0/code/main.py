import http.server
import os
from urllib.parse import urlparse, parse_qs
from user_manager import UserManager
from book_manager import BookManager

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.book_manager = BookManager('books.txt')

    def main(self):
        server_address = ('', 8000)
        httpd = http.server.HTTPServer(server_address, self.RequestHandler)
        print("Starting server on port 8000...")
        httpd.serve_forever()

    class RequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_path = urlparse(self.path)
            if parsed_path.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(open('templates/login.html', 'rb').read())
            elif parsed_path.path == '/register':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(open('templates/registration.html', 'rb').read())
            elif parsed_path.path == '/dashboard':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(open('templates/dashboard.html', 'rb').read())
            elif parsed_path.path == '/create_book':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(open('templates/create_book.html', 'rb').read())
            elif parsed_path.path == '/my_books':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(open('templates/my_books.html', 'rb').read())
            elif parsed_path.path.startswith('/book_details'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(open('templates/book_details.html', 'rb').read())
            elif parsed_path.path == '/about':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(open('templates/about.html', 'rb').read())
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            parsed_path = urlparse(self.path)
            if parsed_path.path == '/login':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                credentials = parse_qs(post_data.decode('utf-8'))
                username = credentials['username'][0]
                password = credentials['password'][0]
                if self.server.user_manager.login(username, password):
                    self.send_response(302)
                    self.send_header('Location', '/dashboard')
                    self.end_headers()
                else:
                    self.send_response(401)
                    self.end_headers()
            elif parsed_path.path == '/register':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                credentials = parse_qs(post_data.decode('utf-8'))
                username = credentials['username'][0]
                password = credentials['password'][0]
                if self.server.user_manager.register(username, password):
                    self.send_response(302)
                    self.send_header('Location', '/')
                    self.end_headers()
                else:
                    self.send_response(400)
                    self.end_headers()
            elif parsed_path.path == '/create_book':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                book_data = parse_qs(post_data.decode('utf-8'))
                title = book_data['title'][0]
                author = book_data['author'][0]
                content = book_data['content'][0]
                username = 'some_user'  # This should be replaced with actual logged-in user
                if self.server.book_manager.create_book(username, title, author, content):
                    self.send_response(302)
                    self.send_header('Location', '/my_books')
                    self.end_headers()
                else:
                    self.send_response(400)
                    self.end_headers()

if __name__ == '__main__':
    Main().main()