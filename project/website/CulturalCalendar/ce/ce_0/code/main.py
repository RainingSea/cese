import http.server
import os
import urllib.parse

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.event_manager = EventManager()
        self.reminder_manager = ReminderManager()
        self.event_manager.load_events()

    def main(self):
        server_address = ('', 8000)
        httpd = http.server.HTTPServer(server_address, self.RequestHandler)
        print("Starting server on port 8000...")
        httpd.serve_forever()

    class RequestHandler(http.server.SimpleHTTPRequestHandler):
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
                self.wfile.write(open('templates/registration.html', 'rb').read())
            elif self.path == '/dashboard':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(open('templates/dashboard.html', 'rb').read())
            elif self.path.startswith('/event/'):
                event_id = self.path.split('/')[-1]
                event_details = self.event_manager.get_event_details(event_id)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(event_details.encode())
            elif self.path == '/reminders':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(open('templates/reminders.html', 'rb').read())
            else:
                self.send_error(404)

        def do_POST(self):
            if self.path == '/register':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode()
                username, password = urllib.parse.parse_qs(post_data).get('username')[0], urllib.parse.parse_qs(post_data).get('password')[0]
                if self.user_manager.register(username, password):
                    self.send_response(302)
                    self.send_header('Location', '/')
                    self.end_headers()
                else:
                    self.send_error(400)
            elif self.path == '/login':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode()
                username, password = urllib.parse.parse_qs(post_data).get('username')[0], urllib.parse.parse_qs(post_data).get('password')[0]
                if self.user_manager.login(username, password):
                    self.send_response(302)
                    self.send_header('Location', '/dashboard')
                    self.end_headers()
                else:
                    self.send_error(401)

if __name__ == "__main__":
    app = Main()
    app.main()