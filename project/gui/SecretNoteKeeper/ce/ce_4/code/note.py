class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.created_at = self.get_current_time()

    def get_current_time(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()