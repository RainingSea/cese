class Project:
    def __init__(self, name: str, description: str, assigned_freelancer: str):
        self.name = name
        self.description = description
        self.assigned_freelancer = assigned_freelancer

    def to_string(self) -> str:
        return f"{self.name}|{self.description}|{self.assigned_freelancer}"