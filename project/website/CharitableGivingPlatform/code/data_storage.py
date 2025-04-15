import os
from models import User, Charity, Donation

class DataStorage:
    def load_users(self) -> list:
        """Load users from the users.txt file."""
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def save_users(self, users: list):
        """Save users to the users.txt file."""
        with open('users.txt', 'w') as file:
            for user in users:
                file.write(f"{user.username}|{user.password}\n")

    def load_charities(self) -> list:
        """Load charities from the charities.txt file."""
        charities = []
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    charities.append(Charity(name, mission, projects.split(',')))
        return charities

    def save_charities(self, charities: list):
        """Save charities to the charities.txt file."""
        with open('charities.txt', 'w') as file:
            for charity in charities:
                projects = ','.join(charity.projects)
                file.write(f"{charity.name}|{charity.mission}|{projects}\n")

    def load_donations(self) -> list:
        """Load donations from the donations.txt file."""
        donations = []
        if os.path.exists('donations.txt'):
            with open('donations.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount, date = line.strip().split('|')
                    user = self.get_user_by_username(username)
                    charity = self.get_charity_by_name(charity_name)
                    if user and charity:
                        donations.append(Donation(user, charity, float(amount), date))
        return donations

    def save_donations(self, donations: list):
        """Save donations to the donations.txt file."""
        with open('donations.txt', 'w') as file:
            for donation in donations:
                file.write(f"{donation.user.username}|{donation.charity.name}|{donation.amount}|{donation.date}\n")

    def get_charity_by_name(self, charity_name: str) -> Charity:
        """Retrieve a charity object by its name."""
        charities = self.load_charities()
        for charity in charities:
            if charity.name == charity_name:
                return charity
        return None

    def get_user_by_username(self, username: str) -> User:
        """Retrieve a user object by its username."""
        users = self.load_users()
        for user in users:
            if user.username == username:
                return user
        return None