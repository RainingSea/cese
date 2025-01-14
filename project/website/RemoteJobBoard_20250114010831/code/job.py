class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def save(self):
        pass  # Not needed for this implementation

    @staticmethod
    def load_all() -> list:
        return []  # Not needed for this implementation