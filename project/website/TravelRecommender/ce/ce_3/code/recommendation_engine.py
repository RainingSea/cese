class Destination:
    def __init__(self, name: str, details: str, cost: float):
        self.name = name
        self.details = details
        self.cost = cost

    def get_details(self):
        return self.details

class RecommendationEngine:
    def __init__(self, destinations: list):
        self.destinations = destinations

    def generate_recommendations(self, preferences: dict):
        # Sample static recommendations based on preferences
        return [Destination("Beach Paradise", "A beautiful beach with clear waters.", 500),
                Destination("Mountain Adventure", "A thrilling mountain climbing experience.", 300)]

    def get_destination_details(self, name: str):
        for destination in self.destinations:
            if destination.name == name:
                return destination.get_details()
        return "Destination not found."