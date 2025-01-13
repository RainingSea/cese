class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save_story(self, username: str, title: str, content: str) -> None:
        with open('stories.txt', 'a') as file:
            file.write(f"{username},{title},{content}\n")

    def edit_story(self, username: str, title: str, content: str) -> None:
        # Placeholder for editing story functionality
        pass