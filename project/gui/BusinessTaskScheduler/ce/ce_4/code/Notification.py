class Notification:
    def __init__(self, message: str, date: str):
        self.message = message
        self.date = date

    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "date": self.date
        }