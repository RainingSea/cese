class Resource:
    """Resource class to handle educational resources."""
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def add_resource(self) -> bool:
        """Add a new resource to the resources.txt file."""
        try:
            with open('resources.txt', 'a') as file:
                file.write(f"{self.title}|{self.url}\n")
            return True
        except Exception as e:
            print(f"Error adding resource: {e}")
            return False

    def get_resources(self) -> list:
        """Retrieve all resources from the resources.txt file."""
        resources = []
        try:
            with open('resources.txt', 'r') as file:
                for line in file:
                    title, url = line.strip().split('|')
                    resources.append({'title': title, 'url': url})
        except Exception as e:
            print(f"Error loading resources: {e}")
        return resources