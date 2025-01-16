class Resource:
    def __init__(self, title, link, description):
        self.title = title
        self.link = link
        self.description = description

    def share_resource(self, title, link, description):
        self.title = title
        self.link = link
        self.description = description