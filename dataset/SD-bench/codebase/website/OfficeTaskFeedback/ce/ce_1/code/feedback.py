class Feedback:
    def __init__(self, user: str, category: str, content: str):
        self.user = user
        self.category = category
        self.content = content
        self.status = "Pending"

    def save(self) -> None:
        with open('feedback.txt', 'a') as f:
            f.write(f"{self.user}|{self.category}|{self.content}|{self.status}\n")

    @staticmethod
    def load_all() -> list:
        feedbacks = []
        try:
            with open('feedback.txt', 'r') as f:
                for line in f:
                    user, category, content, status = line.strip().split('|')
                    feedbacks.append(Feedback(user, category, content))
                    feedbacks[-1].status = status
        except FileNotFoundError:
            pass
        return feedbacks

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        self.save()