class Project:
    def __init__(self, name: str, description: str, assigned_freelancer: str):
        self.name = name
        self.description = description
        self.assigned_freelancer = assigned_freelancer

    def save(self):
        """Saves the project data to the projects file."""
        with open('projects.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.assigned_freelancer}\n")