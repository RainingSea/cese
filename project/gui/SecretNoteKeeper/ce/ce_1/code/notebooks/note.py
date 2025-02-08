class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.timestamp = self._get_timestamp()

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()