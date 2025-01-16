class Destination:
    def __init__(self, name: str, activities: list, climate: str, cost: float):
        self.name = name
        self.activities = activities
        self.climate = climate
        self.cost = cost

    @staticmethod
    def load_all() -> list:
        destinations = []
        try:
            with open('destinations.txt', 'r') as file:
                for line in file:
                    name, activities, climate, cost = line.strip().split('|')
                    activities_list = activities.split(',')
                    destinations.append(Destination(name, activities_list, climate, float(cost)))
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return destinations