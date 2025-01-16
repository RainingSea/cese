class Recommendations:
    def generate(self, preferences) -> list:
        # A mock implementation that returns a static list based on preferences
        return [
            {'destination': 'Beach Paradise', 'activities': ['swimming', 'sunbathing'], 'climate': 'tropical', 'cost': 1500},
            {'destination': 'Mountain Retreat', 'activities': ['hiking', 'sightseeing'], 'climate': 'cool', 'cost': 1200}
        ]

    @staticmethod
    def load() -> list:
        recommendations = []
        with open('recommendations.txt', 'r') as f:
            for line in f:
                recommendations.append(line.strip())
        return recommendations