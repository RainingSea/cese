class Password:
    def __init__(self, account_name: str, password: str, notes: str):
        self.account_name = account_name
        self.password = password
        self.notes = notes

    def get_strength(self) -> str:
        if len(self.password) < 6:
            return "Weak"
        elif len(self.password) < 12:
            return "Moderate"
        else:
            return "Strong"