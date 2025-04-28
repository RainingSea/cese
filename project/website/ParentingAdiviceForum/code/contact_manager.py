import os

class ContactManager:
    def __init__(self):
        self.inquiries = self.load_inquiries()

    def load_inquiries(self):
        if not os.path.exists('contact_inquiries.txt'):
            return []
        with open('contact_inquiries.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def submit_inquiry(self, name: str, email: str, message: str) -> bool:
        self.inquiries.append([name, email, message])
        self.save_inquiries()
        return True

    def save_inquiries(self):
        with open('contact_inquiries.txt', 'w') as file:
            for inquiry in self.inquiries:
                file.write('|'.join(inquiry) + '\n')