class RecommendationEngine:
    def generate_recommendations(self, preferences: dict) -> list:
        recommendations = []
        if preferences.get('budget') == 'low':
            recommendations.append("Local Park")
            recommendations.append("Free Museum")
        elif preferences.get('budget') == 'medium':
            recommendations.append("Beach Resort")
            recommendations.append("City Tour")
        elif preferences.get('budget') == 'high':
            recommendations.append("Luxury Hotel")
            recommendations.append("Exotic Destination")
        return recommendations