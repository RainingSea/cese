class Donation:
    """Donation class to represent a donation made by a user."""
    
    def __init__(self, username: str, charity_name: str, amount: float, date: str):
        self.username = username
        self.charity_name = charity_name
        self.amount = amount
        self.date = date

    def save_to_file(self):
        """Save donation information to the donations.txt file."""
        with open('donations.txt', 'a') as file:
            file.write(f"{self.username}|{self.charity_name}|{self.amount}|{self.date}\n")