class FreelancerManager:
    def __init__(self):
        self.freelancers = self.load_freelancers()

    def load_freelancers(self):
        freelancers = []
        with open('freelancers.txt', 'r') as file:
            for line in file:
                id, name, skills = line.strip().split('|')
                freelancers.append({'id': int(id), 'name': name, 'skills': skills.split(',')})
        return freelancers

    def search_freelancer(self, name: str):
        return [freelancer for freelancer in self.freelancers if name.lower() in freelancer['name'].lower()]

    def get_freelancer_details(self, id: int):
        for freelancer in self.freelancers:
            if freelancer['id'] == id:
                return freelancer
        return None