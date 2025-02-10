class Destination:
    def __init__(self, name: str, details: str):
        self.name = name
        self.details = details

    def save(self) -> None:
        with open('destinations.txt', 'a') as file:
            file.write(f"{self.name}|{self.details}\n")

    @staticmethod
    def load_all() -> list:
        destinations = []
        with open('destinations.txt', 'r') as file:
            for line in file:
                dest_data = line.strip().split('|')
                destinations.append(Destination(dest_data[0], dest_data[1]))
        return destinations