class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.contributions = []

    def add_contribution(self, amount: float):
        self.contributions.append(amount)

    def get_contributions(self) -> list:
        return self.contributions


class Charity:
    def __init__(self, name: str, mission: str):
        self.name = name
        self.mission = mission
        self.projects = []

    def add_project(self, project: str):
        self.projects.append(project)

    def get_details(self) -> dict:
        return {
            "name": self.name,
            "mission": self.mission,
            "projects": self.projects
        }


class Donation:
    def __init__(self, user: User, charity: Charity, amount: float, date: str):
        self.user = user
        self.charity = charity
        self.amount = amount
        self.date = date