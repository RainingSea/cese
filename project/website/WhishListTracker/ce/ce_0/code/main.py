from flask import Flask, render_template, request, redirect, url_for, session
import os

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class WishlistManager:
    def __init__(self):
        self.wishlist = []
        self.load_wishlist()

    def add_item(self, name: str, description: str, price: float) -> None:
        self.wishlist.append({'name': name, 'description': description, 'price': price})
        self.save_wishlist()

    def update_item(self, index: int, name: str, description: str, price: float) -> None:
        if 0 <= index < len(self.wishlist):
            self.wishlist[index] = {'name': name, 'description': description, 'price': price}
            self.save_wishlist()

    def remove_item(self, index: int) -> None:
        if 0 <= index < len(self.wishlist):
            del self.wishlist[index]
            self.save_wishlist()

    def load_wishlist(self) -> None:
        if os.path.exists('wishlist.txt'):
            with open('wishlist.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    self.wishlist.append({'name': name, 'description': description, 'price': float(price)})

    def save_wishlist(self) -> None:
        with open('wishlist.txt', 'w') as file:
            for item in self.wishlist:
                file.write(f"{item['name']}|{item['description']}|{item['price']}\n")

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.wishlist_manager = WishlistManager()
        self.app = Flask(__name__)
        self.app.secret_key = 'supersecretkey'
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                if self.user_manager.login(username, password):
                    session['username'] = username
                    return redirect(url_for('dashboard'))
            return render_template('login.html')

        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                if self.user_manager.register(username, password):
                    return redirect(url_for('login'))
            return render_template('registration.html')

        @self.app.route('/dashboard', methods=['GET', 'POST'])
        def dashboard():
            if 'username' not in session:
                return redirect(url_for('login'))
            if request.method == 'POST':
                if 'add' in request.form:
                    name = request.form['name']
                    description = request.form['description']
                    price = float(request.form['price'])
                    self.wishlist_manager.add_item(name, description, price)
                elif 'remove' in request.form:
                    index = int(request.form['index'])
                    self.wishlist_manager.remove_item(index)
            return render_template('dashboard.html', wishlist=self.wishlist_manager.wishlist)

        @self.app.route('/logout')
        def logout():
            session.pop('username', None)
            return redirect(url_for('login'))

    def main(self) -> str:
        self.app.run(port=8458, debug=False)

if __name__ == "__main__":
    main_app = Main()
    main_app.main()