class StoryManager:
    def __init__(self):
        self.stories = self.load_stories()

    def load_stories(self):
        stories = []
        try:
            with open('stories.txt', 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(',')
                    stories.append({'username': username, 'title': title, 'content': content})
        except FileNotFoundError:
            pass
        return stories

    def create_story(self, username: str, title: str, content: str) -> None:
        with open('stories.txt', 'a') as file:
            file.write(f"{username},{title},{content}\n")
        self.stories.append({'username': username, 'title': title, 'content': content})

    def edit_story(self, username: str, title: str, content: str) -> None:
        for story in self.stories:
            if story['username'] == username and story['title'] == title:
                story['content'] = content
                self.save_story()
                break

    def save_story(self) -> None:
        with open('stories.txt', 'w') as file:
            for story in self.stories:
                file.write(f"{story['username']},{story['title']},{story['content']}\n")