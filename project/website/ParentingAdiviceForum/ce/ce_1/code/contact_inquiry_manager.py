class ContactInquiryManager:
    def __init__(self):
        self.inquiries = self.load_inquiries()

    def load_inquiries(self):
        inquiries = []
        try:
            with open('contact_inquiries.txt', 'r') as file:
                for line in file:
                    name, email, message = line.strip().split('|')
                    inquiries.append({'name': name, 'email': email, 'message': message})
        except FileNotFoundError:
            pass
        return inquiries

    def submit_inquiry(self, name: str, email: str, message: str) -> bool:
        self.inquiries.append({'name': name, 'email': email, 'message': message})
        with open('contact_inquiries.txt', 'a') as file:
            file.write(f"{name}|{email}|{message}\n")
        return True