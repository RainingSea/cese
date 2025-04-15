class Resource:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link

    def share_resource(self):
        """Save the resource to the resources.txt file."""
        with open('resources.txt', 'a') as file:
            file.write(f"{self.title}|{self.link}\n")

    @staticmethod
    def load_resources() -> list:
        """Load resources from the resources.txt file."""
        resources = []
        try:
            with open('resources.txt', 'r') as file:
                for line in file:
                    title, link = line.strip().split('|')
                    resources.append({'title': title, 'link': link})
        except FileNotFoundError:
            return []
        return resources