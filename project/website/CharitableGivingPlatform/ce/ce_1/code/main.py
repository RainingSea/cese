import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.charity_manager = CharityManager()

    def main(self):
        self.load_data()
        # Start the web application (this would typically involve a web framework)
        print("Welcome to the Charitable Giving Platform")

    def load_data(self):
        self.user_manager.load_users()
        self.charity_manager.load_charities()

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append({'username': username, 'password': password})

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def get_user_contributions(self, username: str) -> list:
        contributions = []
        if os.path.exists('donations.txt'):
            with open('donations.txt', 'r') as file:
                for line in file:
                    user, charity, amount = line.strip().split('|')
                    if user == username:
                        contributions.append({'charity': charity, 'amount': float(amount)})
        return contributions

class CharityManager:
    def __init__(self):
        self.charities = []

    def load_charities(self):
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    self.charities.append({'name': name, 'mission': mission, 'projects': projects.split(',')})

    def get_charities(self) -> list:
        return self.charities

    def get_charity_details(self, charity_name: str) -> str:
        for charity in self.charities:
            if charity['name'] == charity_name:
                return f"Mission: {charity['mission']}, Projects: {', '.join(charity['projects'])}"
        return "Charity not found."

    def record_donation(self, username: str, charity_name: str, amount: float) -> None:
        with open('donations.txt', 'a') as file:
            file.write(f"{username}|{charity_name}|{amount}\n")