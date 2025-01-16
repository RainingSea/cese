class Destination:
    def __init__(self, name: str, details: dict):
        self.name = name
        self.details = details

    @staticmethod
    def load_destinations():
        destinations = []
        try:
            with open('destinations.txt', 'r') as file:
                for line in file:
                    name, details_str = line.strip().split('|')
                    details = eval(details_str)  # Assuming details are stored as a dictionary
                    destinations.append(Destination(name, details))
        except FileNotFoundError:
            pass
        return destinations