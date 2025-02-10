class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.applied_jobs = []

    def to_string(self) -> str:
        return f"{self.username}|{self.password}|{self.email}|{','.join(self.applied_jobs)}"

class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def to_string(self) -> str:
        return f"{self.title}|{self.company}|{self.description}"