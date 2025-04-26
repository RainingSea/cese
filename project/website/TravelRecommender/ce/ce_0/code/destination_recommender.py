import os

class DestinationRecommender:
    def __init__(self):
        self.destinations = []

    def get_recommendations(self, preferences: dict) -> list:
        recommendations = []
        for destination in self.destinations:
            if (destination['cost'] <= preferences['budget'] and
                destination['climate'] == preferences['climate'] and
                any(activity in destination['activities'] for activity in preferences['activities'])):
                recommendations.append(destination)
        return recommendations

    def load_destinations(self) -> None:
        if os.path.exists('destinations.txt'):
            with open('destinations.txt', 'r') as file:
                for line in file:
                    name, activities, climate, cost = line.strip().split('|')
                    self.destinations.append({
                        'name': name,
                        'activities': activities.split(','),
                        'climate': climate,
                        'cost': int(cost)
                    })