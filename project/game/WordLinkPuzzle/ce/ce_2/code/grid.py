class Grid:
    def __init__(self):
        self.letters = self.generate_letters()

    def generate_letters(self):
        # Generate a 4x4 grid of random letters (for simplicity)
        import random
        import string
        return [[random.choice(string.ascii_uppercase) for _ in range(4)] for _ in range(4)]

    def connect_letters(self):
        # Handle user input for connecting letters (not implemented for brevity)
        pass