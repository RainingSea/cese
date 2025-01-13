class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'company': self.company,
            'description': self.description
        }