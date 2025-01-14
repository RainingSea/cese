class Contact:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def save(self):
        with open('contacts.txt', 'a') as file:
            file.write(f"{self.name}|{self.email}|{self.message}\n")