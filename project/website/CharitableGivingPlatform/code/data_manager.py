from user import User
from charity import Charity
from donation import Donation

class DataManager:
    def load_users(self) -> list:
        return User.load_users()

    def save_users(self, users: list):
        with open('users.txt', 'w') as file:
            for user in users:
                file.write(f"{user.username}|{user.password}\n")

    def load_charities(self) -> list:
        return Charity.load_charities()

    def save_charities(self, charities: list):
        with open('charities.txt', 'w') as file:
            for charity in charities:
                file.write(f"{charity.name}|{charity.mission}\n")

    def load_donations(self) -> list:
        donations = []
        try:
            with open('donations.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount, date = line.strip().split('|')
                    donations.append(Donation(username, charity_name, float(amount), date))
        except FileNotFoundError:
            return []
        return donations

    def save_donations(self, donations: list):
        with open('donations.txt', 'a') as file:
            for donation in donations:
                file.write(f"{donation.user}|{donation.charity}|{donation.amount}|{donation.date}\n")