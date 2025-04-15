class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.contributions = []

    def add_contribution(self, amount: float):
        """Add a contribution amount to the user's contribution history."""
        self.contributions.append(amount)

    def get_contribution_history(self) -> list:
        """Return the user's contribution history."""
        return self.contributions


class Charity:
    def __init__(self, name: str, mission: str, projects: list):
        self.name = name
        self.mission = mission
        self.projects = projects

    def get_details(self) -> dict:
        """Return the details of the charity."""
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