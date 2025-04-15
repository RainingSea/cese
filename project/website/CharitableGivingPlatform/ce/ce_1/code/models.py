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
    def __init__(self, name: str, mission: str, projects: list):
        self.name = name
        self.mission = mission
        self.projects = projects

    def get_details(self) -> dict:
        return {
            'name': self.name,
            'mission': self.mission,
            'projects': self.projects
        }


class Donation:
    def __init__(self, username: str, charity_name: str, amount: float, date: str):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount
        self.date = date


class UserStorage:
    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")

    def get_user(self, username: str) -> User:
        users = self.load_users()
        for user in users:
            if user.username == username:
                return user
        return None


class CharityStorage:
    def load_charities(self) -> list:
        charities = []
        try:
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    charities.append(Charity(name, mission, projects.split(',')))
        except FileNotFoundError:
            pass
        return charities

    def save_charity(self, charity: Charity):
        with open('charities.txt', 'a') as file:
            projects = ','.join(charity.projects)
            file.write(f"{charity.name}|{charity.mission}|{projects}\n")

    def get_charity(self, name: str) -> Charity:
        charities = self.load_charities()
        for charity in charities:
            if charity.name == name:
                return charity
        return None


class DonationStorage:
    def load_donations(self) -> list:
        donations = []
        try:
            with open('donations.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount, date = line.strip().split('|')
                    donations.append(Donation(username, charity_name, float(amount), date))
        except FileNotFoundError:
            pass
        return donations

    def save_donation(self, donation: Donation):
        with open('donations.txt', 'a') as file:
            file.write(f"{donation.username}|{donation.charity_name}|{donation.amount}|{donation.date}\n")

    def get_user_donations(self, username: str) -> list:
        donations = self.load_donations()
        return [donation for donation in donations if donation.username == username]