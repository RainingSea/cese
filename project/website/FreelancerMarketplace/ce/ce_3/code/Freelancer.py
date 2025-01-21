class Freelancer:
    def __init__(self, name: str, skills: list):
        self.name = name
        self.skills = skills

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "skills": self.skills
        }