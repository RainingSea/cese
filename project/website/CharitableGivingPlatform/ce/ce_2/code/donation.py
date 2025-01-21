class Donation:
    def __init__(self, username: str, charity_name: str, amount: float):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount

    def save_donation(self):
        with open('donations.txt', 'a') as f:
            f.write(f"{self.username}|{self.charity_name}|{self.amount}\n")

    @staticmethod
    def load_donations() -> list:
        donations = []
        try:
            with open('donations.txt', 'r') as f:
                for line in f:
                    username, charity_name, amount = line.strip().split('|')
                    donations.append(Donation(username, charity_name, float(amount)))
        except FileNotFoundError:
            pass
        return donations