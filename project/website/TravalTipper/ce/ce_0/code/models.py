class TravelTip:
    def __init__(self, destination: str, trip_duration: str, interests: list, customs: str,
                 safety_tips: str, transportation: str, etiquette: str, attractions: str):
        self.destination = destination
        self.trip_duration = trip_duration
        self.interests = interests
        self.customs = customs
        self.safety_tips = safety_tips
        self.transportation = transportation
        self.etiquette = etiquette
        self.attractions = attractions


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.favorites = []

    def add_favorite(self, tip: TravelTip):
        self.favorites.append(tip)

    def remove_favorite(self, tip: TravelTip):
        self.favorites.remove(tip)