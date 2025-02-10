class MovieRecommendation:
    def __init__(self, user_preferences: dict):
        self.user_preferences = user_preferences

    def recommend_movies(self):
        # For simplicity, returning a static list of movie titles
        return ['Movie A', 'Movie B', 'Movie C']