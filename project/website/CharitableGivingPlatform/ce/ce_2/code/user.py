class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.contributions = []

    def add_contribution(self, amount: float):
        self.contributions.append(amount)

    def get_contribution_history(self):
        return self.contributions