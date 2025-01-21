class Freelancer:
    def __init__(self, name: str, skills: list):
        self.name = name
        self.skills = skills

    def save(self):
        """Saves the freelancer data to the freelancers file."""
        with open('freelancers.txt', 'a') as file:
            skills_str = ','.join(self.skills)
            file.write(f"{self.name}|{skills_str}\n")