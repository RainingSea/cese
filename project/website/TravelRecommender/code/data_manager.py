import json
from models import User, Preferences, Destination, Favorites

class DataManager:
    def load_users(self) -> list:
        try:
            with open('users.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_users(self, users: list):
        with open('users.json', 'w') as file:
            json.dump(users, file)

    def load_preferences(self) -> dict:
        try:
            with open('preferences.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_preferences(self, preferences: dict):
        with open('preferences.json', 'w') as file:
            json.dump(preferences, file)

    def load_destinations(self) -> list:
        try:
            with open('destinations.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_destinations(self, destinations: list):
        with open('destinations.json', 'w') as file:
            json.dump(destinations, file)

    def load_favorites(self, user: str) -> list:
        try:
            with open('favorites.json', 'r') as file:
                favorites_data = json.load(file)
                return favorites_data.get(user, [])
        except FileNotFoundError:
            return []

    def save_favorites(self, user: str, favorites: list):
        try:
            with open('favorites.json', 'r') as file:
                favorites_data = json.load(file)
        except FileNotFoundError:
            favorites_data = {}
        favorites_data[user] = favorites
        with open('favorites.json', 'w') as file:
            json.dump(favorites_data, file)