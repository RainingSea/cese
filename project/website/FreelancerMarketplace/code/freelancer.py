class Freelancer:
    def __init__(self, name: str, skills: list):
        self.name = name
        self.skills = skills

    def save(self):
        with open('freelancers.txt', 'a') as file:
            skills_str = ','.join(self.skills)
            file.write(f"{self.name}|{skills_str}\n")

    @staticmethod
    def load(name: str):
        with open('freelancers.txt', 'r') as file:
            for line in file:
                freelancer_data = line.strip().split('|')
                if freelancer_data[0] == name:
                    return Freelancer(freelancer_data[0], freelancer_data[1].split(','))
        return None