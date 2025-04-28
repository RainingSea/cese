class FeedbackManager:
    def __init__(self, filename):
        self.filename = filename

    def submit_feedback(self, user, feedback):
        with open(self.filename, 'a') as file:
            file.write(f"{user}|{feedback}\n")