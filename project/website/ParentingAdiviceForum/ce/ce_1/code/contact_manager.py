class ContactManager:
    def __init__(self, filename):
        self.filename = filename

    def submit_contact(self, name, email, message):
        with open(self.filename, 'a') as file:
            file.write(f"{name}|{email}|{message}\n")
        return True