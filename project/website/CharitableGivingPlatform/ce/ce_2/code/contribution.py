import os

class Contribution:
    def __init__(self):
        self.contributions = []

    def load_contributions(self):
        if os.path.exists('contributions.txt'):
            with open('contributions.txt', 'r') as file:
                for line in file:
                    username, charity_id, amount = line.strip().split('|')
                    self.contributions.append({'username': username, 'charity_id': charity_id, 'amount': float(amount)})

    def add_contribution(self, username: str, charity_id: str, amount: float):
        self.contributions.append({'username': username, 'charity_id': charity_id, 'amount': amount})
        with open('contributions.txt', 'a') as file:
            file.write(f"{username}|{charity_id}|{amount}\n")