class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.contributions = []

    def add_contribution(self, amount: float):
        self.contributions.append(amount)

    def get_contributions(self) -> list:
        return self.contributions


class Charity:
    def __init__(self, name: str, mission: str):
        self.name = name
        self.mission = mission
        self.projects = []

    def add_project(self, project: str):
        self.projects.append(project)

    def get_details(self) -> dict:
        return {
            'name': self.name,
            'mission': self.mission,
            'projects': self.projects
        }


class Donation:
    def __init__(self, username: str, charity_name: str, amount: float):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount


class DataStorage:
    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}|{','.join(map(str, user.get_contributions()))}\n")

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, contributions = line.strip().split('|')
                    user = User(username, password)
                    user.contributions = list(map(float, contributions.split(','))) if contributions else []
                    users.append(user)
        except FileNotFoundError:
            pass
        return users

    def save_charity(self, charity: Charity):
        with open('charities.txt', 'a') as file:
            file.write(f"{charity.name}|{charity.mission}|{','.join(charity.projects)}\n")

    def load_charities(self) -> list:
        charities = []
        try:
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    charity = Charity(name, mission)
                    charity.projects = projects.split(',') if projects else []
                    charities.append(charity)
        except FileNotFoundError:
            pass
        return charities

    def save_donation(self, donation: Donation):
        with open('donations.txt', 'a') as file:
            file.write(f"{donation.username}|{donation.charity_name}|{donation.amount}\n")

    def load_donations(self) -> list:
        donations = []
        try:
            with open('donations.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount = line.strip().split('|')
                    donation = Donation(username, charity_name, float(amount))
                    donations.append(donation)
        except FileNotFoundError:
            pass
        return donations