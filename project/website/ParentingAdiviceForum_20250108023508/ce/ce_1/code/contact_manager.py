class ContactInquiry:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

class ContactManager:
    def __init__(self):
        self.inquiries = []

    def add_inquiry(self, inquiry: ContactInquiry):
        self.inquiries.append(inquiry)
        with open('contact_inquiries.txt', 'a') as file:
            file.write(f"{inquiry.name}|{inquiry.email}|{inquiry.message}\n")