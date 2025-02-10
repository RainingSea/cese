import os

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.contributions = []

    def add_contribution(self, donation: float):
        self.contributions.append(donation)

class Charity:
    def __init__(self, name: str, mission: str):
        self.name = name
        self.mission = mission
        self.projects = []

    def add_project(self, project: str):
        self.projects.append(project)

class Donation:
    def __init__(self, username: str, charity_name: str, amount: float):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount

class DataManager:
    def load_users(self) -> list:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def save_users(self, users: list):
        with open('users.txt', 'w') as file:
            for user in users:
                file.write(f"{user.username}|{user.password}\n")

    def load_charities(self) -> list:
        charities = []
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission = line.strip().split('|')
                    charities.append(Charity(name, mission))
        return charities

    def save_charities(self, charities: list):
        with open('charities.txt', 'w') as file:
            for charity in charities:
                file.write(f"{charity.name}|{charity.mission}\n")

    def load_donations(self) -> list:
        donations = []
        if os.path.exists('donations.txt'):
            with open('donations.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount = line.strip().split('|')
                    donations.append(Donation(username, charity_name, float(amount)))
        return donations

    def save_donations(self, donations: list):
        with open('donations.txt', 'w') as file:
            for donation in donations:
                file.write(f"{donation.username}|{donation.charity_name}|{donation.amount}\n")