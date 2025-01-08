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
        with open('contact_inquiries.txt', 'r') as file:
            for line in file:
                name, email, message = line.strip().split('|')
                inquiries.append(ContactInquiry(name, email, message))
        return inquiries

    def add_inquiry(self, inquiry: ContactInquiry):
        self.inquiries.append(inquiry)
        with open('contact_inquiries.txt', 'a') as file:
            file.write(f"{inquiry.name}|{inquiry.email}|{inquiry.message}\n")