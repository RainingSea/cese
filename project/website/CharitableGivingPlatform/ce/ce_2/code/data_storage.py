import os
from user import User
from charity import Charity
from donation import Donation

class UserStorage:
    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def save_user(self, user):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")

class CharityStorage:
    def load_charities(self):
        charities = []
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    charities.append(Charity(name, mission, projects.split(',')))
        return charities

    def save_charity(self, charity):
        with open('charities.txt', 'a') as file:
            file.write(f"{charity.name}|{charity.mission}|{','.join(charity.projects)}\n")

class DonationStorage:
    def load_donations(self):
        donations = []
        if os.path.exists('donations.txt'):
            with open('donations.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount, date = line.strip().split('|')
                    donations.append(Donation(username, charity_name, float(amount), date))
        return donations

    def save_donation(self, donation):
        with open('donations.txt', 'a') as file:
            file.write(f"{donation.user}|{donation.charity.name}|{donation.amount}|{donation.date}\n")