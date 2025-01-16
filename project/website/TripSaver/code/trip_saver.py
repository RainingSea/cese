from user import User
from trip import Trip
from transportation_option import TransportationOption

class TripSaver:
    def register_user(self, username: str, password: str) -> bool:
        if self.load_user(username) is not None:
            return False
        user = User(username, password)
        user.save()
        return True

    def login_user(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and user.password == password:
            return True
        return False

    def input_trip(self, starting_point: str, destination: str, travel_date: str) -> None:
        trip = Trip(starting_point, destination, travel_date)
        trip.save()

    def get_transportation_options(self) -> list:
        options = []
        with open('transportation_options.txt', 'r') as file:
            for line in file:
                mode, cost, time = line.strip().split('|')
                options.append(TransportationOption(mode, float(cost), float(time)))
        return options

    def load_user(self, username: str) -> User:
        return User.load(username)

    def save_preferred_transportation_option(self, username: str, preferred_option: str) -> None:
        with open('preferred_transportation_options.txt', 'a') as file:
            file.write(f"{username}|{preferred_option}\n")

    def calculate_estimated_costs(self, options: list) -> dict:
        estimated_costs = {}
        for option in options:
            estimated_costs[option.mode] = {
                'cost': option.cost,
                'time': option.time
            }
        return estimated_costs