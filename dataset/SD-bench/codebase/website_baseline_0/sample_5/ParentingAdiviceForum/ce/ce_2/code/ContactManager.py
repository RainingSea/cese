import json
import os

class ContactManager:
    def __init__(self, data_file='contacts.txt'):
        self.data_file = data_file
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.contacts = [json.loads(line.strip()) for line in file.readlines()]
        else:
            self.contacts = []

    def submit_contact(self, name: str, email: str, message: str) -> bool:
        contact = {'name': name, 'email': email, 'message': message}
        self.contacts.append(contact)
        self.save_contacts()
        return True

    def get_contacts(self) -> list:
        return self.contacts

    def save_contacts(self):
        with open(self.data_file, 'w') as file:
            for contact in self.contacts:
                file.write(json.dumps(contact) + '\n')