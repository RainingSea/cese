from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from user_manager import UserManager
from book_manager import BookManager

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'supersecretkey'
        self.app.config['SESSION_TYPE'] = 'filesystem'
        Session(self.app)
        self.user_manager = UserManager('users.txt')
        self.book_manager = BookManager('books.txt')
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def login():
            return render_template('login.html')

        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                if self.user_manager.register(username, password):
                    return redirect('/')
            return render_template('registration.html')

        @self.app.route('/dashboard', methods=['GET', 'POST'])
        def dashboard():
            if 'username' not in session:
                return redirect('/')
            if request.method == 'POST':
                query = request.form['query']
                books = self.book_manager.search_books(query)
                return render_template('dashboard.html', books=books)
            return render_template('dashboard.html')

        @self.app.route('/login', methods=['POST'])
        def do_login():
            username = request.form['username']
            password = request.form['password']
            if self.user_manager.login(username, password):
                session['username'] = username
                return redirect('/dashboard')
            return redirect('/')

        @self.app.route('/reading_list')
        def reading_list():
            if 'username' not in session:
                return redirect('/')
            reading_list = self.user_manager.load_reading_list(session['username'])
            return render_template('reading_list.html', reading_list=reading_list)

    def main(self):
        self.app.run(port=8289, debug=False)

if __name__ == '__main__':
    main_instance = Main()
    main_instance.main()