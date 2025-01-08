class ContactInquiry:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

class ContactManager:
    def __init__(self):
        self.inquiries = self.load_inquiries()

    def load_inquiries(self):
        inquiries = []
        try:
            with open('contact_inquiries.txt', 'r') as file:
                for line in file:
                    name, email, message = line.strip().split('|')
                    inquiries.append(ContactInquiry(name, email, message))
        except FileNotFoundError:
            pass
        return inquiries

    def add_inquiry(self, name: str, email: str, message: str):
        new_inquiry = ContactInquiry(name, email, message)
        self.inquiries.append(new_inquiry)
        with open('contact_inquiries.txt', 'a') as file:
            file.write(f"{name}|{email}|{message}\n")