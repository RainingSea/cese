class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'password': self.password
        }

class Preferences:
    def __init__(self, budget: float, activities: list, climate: str):
        self.budget = budget
        self.activities = activities
        self.climate = climate

    def to_dict(self) -> dict:
        return {
            'budget': self.budget,
            'activities': self.activities,
            'climate': self.climate
        }

class Destination:
    def __init__(self, name: str, activities: list, climate: str, cost: float):
        self.name = name
        self.activities = activities
        self.climate = climate
        self.cost = cost

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'activities': self.activities,
            'climate': self.climate,
            'cost': self.cost
        }

class RecommendationEngine:
    def __init__(self, destinations: list):
        self.destinations = destinations

    def generate_recommendations(self, preferences: Preferences) -> list:
        recommendations = []
        for destination in self.destinations:
            if destination['cost'] <= preferences.budget and destination['climate'] == preferences.climate:
                recommendations.append(Destination(destination['name'], destination['activities'], destination['climate'], destination['cost']))
        return recommendations

class Favorites:
    def __init__(self, user: str):
        self.user = user
        self.favorites = []

    def add_favorite(self, destination: Destination):
        self.favorites.append(destination.to_dict())

    def get_favorites(self) -> list:
        return self.favorites