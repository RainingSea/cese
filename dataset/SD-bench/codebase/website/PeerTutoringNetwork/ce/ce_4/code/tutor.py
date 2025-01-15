class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def save(self):
        with open('tutors.txt', 'a') as f:
            f.write(f"{self.name}|{self.subject}\n")