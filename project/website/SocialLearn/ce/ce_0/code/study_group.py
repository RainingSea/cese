class StudyGroup:
    def __init__(self, name: str):
        self.name = name
        self.members = []

    def add_member(self, username: str):
        self.members.append(username)

    def save(self):
        pass  # Saving handled in main.py