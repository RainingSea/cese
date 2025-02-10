class Donation:
    def __init__(self, username: str, charity_name: str, amount: float):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount

    def save(self) -> None:
        with open('donations.txt', 'a') as file:
            file.write(f"{self.username}|{self.charity_name}|{self.amount}\n")

    @staticmethod
    def load_user_history(username: str) -> list:
        donations = []
        with open('donations.txt', 'r') as file:
            for line in file:
                user, charity_name, amount = line.strip().split('|')
                if user == username:
                    donations.append(Donation(user, charity_name, float(amount)))
        return donations