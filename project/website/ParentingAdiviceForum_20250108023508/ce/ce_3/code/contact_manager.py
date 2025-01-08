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

    def add_inquiry(self, inquiry: ContactInquiry):
        self.inquiries.append(inquiry)
        self.save_inquiries()

    def save_inquiries(self):
        with open('contact_inquiries.txt', 'w') as file:
            for inquiry in self.inquiries:
                file.write(f"{inquiry.name}|{inquiry.email}|{inquiry.message}\n")