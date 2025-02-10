from destination import Destination

class RecommendationEngine:
    @staticmethod
    def generate_recommendations(preferences):
        destinations = Destination.load_destinations()
        recommendations = []
        for destination in destinations:
            if preferences.budget >= destination.details.get('cost', float('inf')) and \
               set(preferences.activities).intersection(destination.details.get('activities', [])):
                recommendations.append(destination)
        return recommendations