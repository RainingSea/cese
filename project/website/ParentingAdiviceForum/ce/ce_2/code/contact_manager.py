class ContactManager:
    def __init__(self):
        self.contacts = self.load_contacts()

    def load_contacts(self):
        contacts = []
        try:
            with open('contacts.txt', 'r') as file:
                for line in file:
                    contacts.append(line.strip().split('|'))
        except FileNotFoundError:
            pass
        return contacts

    def submit_contact(self, name: str, email: str, message: str) -> bool:
        self.contacts.append((name, email, message))
        self.save_contacts()
        return True

    def save_contacts(self):
        with open('contacts.txt', 'w') as file:
            for contact in self.contacts:
                file.write(f"{contact[0]}|{contact[1]}|{contact[2]}\n")