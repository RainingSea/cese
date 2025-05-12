class ContactManager:
    def __init__(self):
        self.contacts = self.load_contacts()

    def load_contacts(self):
        contacts = []
        try:
            with open('contacts.txt', 'r') as file:
                for line in file:
                    name, email, message = line.strip().split('|')
                    contacts.append({'name': name, 'email': email, 'message': message})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return contacts

    def submit_contact(self, name: str, email: str, message: str) -> bool:
        self.contacts.append({'name': name, 'email': email, 'message': message})
        self.save_contacts()
        return True

    def save_contacts(self):
        with open('contacts.txt', 'w') as file:
            for contact in self.contacts:
                file.write(f"{contact['name']}|{contact['email']}|{contact['message']}\n")