class Project:
    def __init__(self, name: str, description: str, freelancer: str):
        self.name = name
        self.description = description
        self.freelancer = freelancer

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "freelancer": self.freelancer
        }