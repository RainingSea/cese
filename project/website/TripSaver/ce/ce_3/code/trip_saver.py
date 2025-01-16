from user import User
from trip import Trip
from transportation_option import TransportationOption

class TripSaver:
    def __init__(self):
        self.users = self.load_users()
        self.trips = []
        self.suggestions = self.load_suggestions()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def load_suggestions(self):
        suggestions = []
        try:
            with open('suggestions.txt', 'r') as f:
                for line in f:
                    mode, cost, time = line.strip().split('|')
                    suggestions.append(TransportationOption(mode, float(cost), float(time)))
        except FileNotFoundError:
            pass
        return suggestions

    def register(self, username: str, password: str):
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def input_trip(self, starting_point: str, destination: str, travel_date: str):
        new_trip = Trip(starting_point, destination, travel_date)
        new_trip.save()
        self.trips.append(new_trip)

    def get_suggestions(self) -> list:
        return self.suggestions

    def compare_options(self) -> list:
        # Placeholder for comparison logic
        return self.suggestions

    def save_preferred_option(self, option: TransportationOption):
        with open('suggestions.txt', 'a') as f:
            f.write(f"{option.mode}|{option.cost}|{option.time}\n")