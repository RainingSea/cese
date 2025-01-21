class Donation:
    def __init__(self, user_id: str, charity_id: int, amount: float):
        self.user_id = user_id
        self.charity_id = charity_id
        self.amount = amount

    def save(self):
        with open('donations.txt', 'a') as file:
            file.write(f"{self.user_id}|{self.charity_id}|{self.amount}\n")

    @staticmethod
    def load_all() -> list:
        donations = []
        with open('donations.txt', 'r') as file:
            for line in file:
                user_id, charity_id, amount = line.strip().split('|')
                donations.append(Donation(user_id, int(charity_id), float(amount)))
        return donations