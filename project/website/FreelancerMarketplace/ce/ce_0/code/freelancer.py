class Freelancer:
    def __init__(self, name: str, details: str):
        self.name = name
        self.details = details

    def save(self):
        with open('freelancers.txt', 'a') as file:
            file.write(f"{self.name}|{self.details}\n")

    @staticmethod
    def load(name: str):
        with open('freelancers.txt', 'r') as file:
            for line in file:
                freelancer_data = line.strip().split('|')
                if freelancer_data[0] == name:
                    return Freelancer(freelancer_data[0], freelancer_data[1])
        return None