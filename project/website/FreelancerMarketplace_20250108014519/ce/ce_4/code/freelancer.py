class Freelancer:
    def __init__(self, name: str, details: str):
        self.name = name
        self.details = details

    def save(self):
        with open('freelancers.txt', 'a') as f:
            f.write(f"{self.name}|{self.details}\n")

    @staticmethod
    def load_all() -> list:
        freelancers = []
        with open('freelancers.txt', 'r') as f:
            for line in f:
                name, details = line.strip().split('|')
                freelancers.append(Freelancer(name, details))
        return freelancers