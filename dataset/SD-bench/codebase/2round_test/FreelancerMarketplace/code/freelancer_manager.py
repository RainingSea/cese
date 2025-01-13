class Freelancer:
    def __init__(self, name: str, details: str):
        self.name = name
        self.details = details

    def save(self):
        with open('freelancers.txt', 'a') as f:
            f.write(f"{self.name}|{self.details}\n")


class FreelancerManager:
    def add_freelancer(self, name: str, details: str) -> None:
        freelancer = Freelancer(name, details)
        freelancer.save()

    def load_freelancers(self) -> list:
        freelancers = []
        try:
            with open('freelancers.txt', 'r') as f:
                for line in f:
                    name, details = line.strip().split('|')
                    freelancers.append(Freelancer(name, details))
        except FileNotFoundError:
            pass
        return freelancers

    def search_freelancers(self, criteria: str) -> list:
        freelancers = self.load_freelancers()
        return [freelancer for freelancer in freelancers if criteria.lower() in freelancer.name.lower()]