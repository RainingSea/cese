class Freelancer:
    def __init__(self, name: str, details: str):
        self.name = name
        self.details = details

    def save(self):
        with open('freelancers.txt', 'a') as f:
            f.write(f'{self.name}|{self.details}\n')


class FreelancerManager:
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

    def search_freelancer(self, name: str) -> Freelancer:
        freelancers = self.load_freelancers()
        for freelancer in freelancers:
            if freelancer.name == name:
                return freelancer
        return None