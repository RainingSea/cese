class Contribution:
    def __init__(self, username: str, charity_name: str, amount: float):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount

    def save(self):
        with open('contributions.txt', 'a') as file:
            file.write(f"{self.username}|{self.charity_name}|{self.amount}\n")

    @staticmethod
    def load_contributions() -> list:
        contributions = []
        try:
            with open('contributions.txt', 'r') as file:
                for line in file:
                    username, charity_name, amount = line.strip().split('|')
                    contributions.append(Contribution(username, charity_name, float(amount)))
        except FileNotFoundError:
            pass
        return contributions