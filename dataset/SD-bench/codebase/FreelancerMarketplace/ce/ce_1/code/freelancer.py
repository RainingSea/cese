class Freelancer:
    def __init__(self, name: str, details: str):
        self.name = name
        self.details = details

    def save(self):
        with open('freelancers.txt', 'a') as file:
            file.write(f"{self.name}|{self.details}\n")

    @staticmethod
    def load_freelancers():
        freelancers = []
        with open('freelancers.txt', 'r') as file:
            for line in file:
                name, details = line.strip().split('|')
                freelancers.append(Freelancer(name, details))
        return freelancers