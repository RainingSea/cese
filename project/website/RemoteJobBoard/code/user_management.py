from data_storage import DataStorage
from flask import session

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.applied_jobs = []

    def save(self) -> None:
        """Saves the user to the data storage."""
        DataStorage.write_user(self.username, self.password, self.email)

    @staticmethod
    def load(username: str) -> 'User':
        """Loads a user from the data storage."""
        users = DataStorage.read_users()
        for user in users:
            if user[0] == username:
                return User(user[0], user[1], user[2])
        return None

    def apply(self, job_id: str) -> None:
        """Applies for a job and saves the application."""
        self.applied_jobs.append(job_id)
        DataStorage.write_application(self.username, job_id)

    def load_applied_jobs(self) -> None:
        """Loads the jobs applied by the user."""
        applications = DataStorage.read_applications()
        for application in applications:
            if application[0] == self.username:
                self.applied_jobs.append(application[1])

    def update_profile(self, new_password: str, new_email: str) -> None:
        """Updates the user's profile information."""
        self.password = new_password
        self.email = new_email
        DataStorage.update_user(self.username, new_password, new_email)

class Auth:
    @staticmethod
    def login(username: str, password: str) -> bool:
        """Logs in a user if the credentials are correct."""
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return True
        return False

    @staticmethod
    def register(username: str, password: str, email: str) -> None:
        """Registers a new user."""
        new_user = User(username, password, email)
        new_user.save()

    @staticmethod
    def logout() -> None:
        """Logs out the current user."""
        session.pop('username', None)

    @staticmethod
    def view_profile(username: str) -> User:
        """Views the profile of the specified user."""
        user = User.load(username)
        if user:
            user.load_applied_jobs()
        return user