import os
from models import User, Charity, Donation

class UserStorage:
    def load_users(self) -> list:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")


class CharityStorage:
    def load_charities(self) -> list:
        charities = []
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission = line.strip().split('|')
                    charities.append(Charity(name, mission))
        return charities

    def save_charity(self, charity: Charity):
        with open('charities.txt', 'a') as file:
            file.write(f"{charity.name}|{charity.mission}\n")


class DonationStorage:
    def load_donations(self) -> list:
        donations = []
        if os.path.exists('donations.txt'):
            with open('donations.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount, date = line.strip().split('|')
                    donations.append(Donation(username, charity_name, float(amount), date))
        return donations

    def save_donation(self, donation: Donation):
        with open('donations.txt', 'a') as file:
            file.write(f"{donation.user.username}|{donation.charity.name}|{donation.amount}|{donation.date}\n")