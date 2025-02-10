class Resource:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link

    def save(self):
        with open('resources.txt', 'a') as file:
            file.write(f"{self.title}|{self.link}\n")