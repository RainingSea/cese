class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save_story(self):
        with open('stories.txt', 'a') as file:
            file.write(f"{self.username}|{self.title}|{self.content}\n")

    def load_stories(self):
        stories = []
        with open('stories.txt', 'r') as file:
            for line in file:
                username, title, content = line.strip().split('|')
                stories.append(Story(username, title, content))
        return stories