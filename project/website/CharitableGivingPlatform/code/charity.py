class Charity:
    """Charity class to represent a charity organization."""
    
    def __init__(self, name: str, mission: str, ongoing_projects: list):
        self.name = name
        self.mission = mission
        self.ongoing_projects = ongoing_projects

    def save_to_file(self):
        """Save charity information to the charities.txt file."""
        with open('charities.txt', 'a') as file:
            file.write(f"{self.name}|{self.mission}|{','.join(self.ongoing_projects)}\n")

    @staticmethod
    def load_from_file():
        """Load charities from the charities.txt file."""
        charities = []
        with open('charities.txt', 'r') as file:
            for line in file:
                name, mission, ongoing_projects = line.strip().split('|')
                charities.append(Charity(name, mission, ongoing_projects.split(',')))
        return charities