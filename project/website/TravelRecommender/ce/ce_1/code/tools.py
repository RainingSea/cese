import os

class UserManager:
    def __init__(self):
        self.users = self.load_user_data()

    def load_user_data(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_user_data()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def save_user_data(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class RecommendationEngine:
    def __init__(self):
        self.destinations = self.load_destinations()

    def load_destinations(self) -> list:
        destinations = []
        if os.path.exists('destinations.txt'):
            with open('destinations.txt', 'r') as file:
                for line in file:
                    destinations.append(line.strip())
        return destinations

    def generate_recommendations(self, preferences: dict) -> list:
        # Simple recommendation logic based on preferences
        recommendations = []
        for destination in self.destinations:
            if preferences['budget'] in destination and preferences['activities'] in destination:
                recommendations.append(destination)
        return recommendations