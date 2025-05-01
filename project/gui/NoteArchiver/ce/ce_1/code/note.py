class Note:
    def __init__(self, content, tags=None):
        self.content = content
        self.tags = tags if tags else []
        self.id = self.generate_id()

    def generate_id(self):
        import uuid
        return str(uuid.uuid4())

    def get_content(self):
        return self.content

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)