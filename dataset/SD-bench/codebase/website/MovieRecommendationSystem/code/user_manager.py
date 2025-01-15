class UserManager:
    """Manages user registration, login, and user data."""
    
    def __init__(self, filename: str):
        """Initializes UserManager with a filename to load users."""
        self.filename = filename
        self.users = self.load_users()

    def load_users(self) -> dict:
        """Loads users from the specified file."""
        users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        """Registers a new user if the username is not taken."""
        if username not in self.users:
            self.users[username] = password
            self.save_users()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        """Logs in a user if the credentials are correct."""
        return username in self.users and self.users[username] == password

    def save_users(self):
        """Saves the current user data to the specified file."""
        with open(self.filename, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

    def get_favorites(self, username: str, favorites_manager) -> list:
        """Retrieves the favorite movies of a user."""
        return favorites_manager.get_favorites(username) if username in self.users else []

    def view_movie_details(self, title: str, movie_manager) -> dict:
        """Retrieves the details of a specific movie."""
        return movie_manager.get_movie_details(title)

    def remove_favorite(self, username: str, movie_title: str, favorites_manager) -> bool:
        """Removes a movie from the user's favorites."""
        return favorites_manager.remove_favorite(username, movie_title)