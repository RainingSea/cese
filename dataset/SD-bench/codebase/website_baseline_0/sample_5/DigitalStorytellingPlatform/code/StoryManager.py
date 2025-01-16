class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('stories.txt', 'a') as file:
            file.write(f"{self.username}|{self.title}|{self.content}\n")

    @staticmethod
    def load_stories() -> list:
        stories = []
        try:
            with open('stories.txt', 'r') as file:
                for line in file:
                    username, title, content = line.strip().split('|', 2)
                    stories.append(Story(username, title, content))
        except FileNotFoundError:
            pass
        return stories


class StoryManager:
    def __init__(self):
        self.stories = Story.load_stories()

    def create_story(self, username: str, title: str, content: str) -> None:
        new_story = Story(username, title, content)
        new_story.save()
        self.stories.append(new_story)

    def edit_story(self, username: str, title: str, new_content: str) -> None:
        for story in self.stories:
            if story.username == username and story.title == title:
                story.content = new_content
                self.save_all_stories()
                break

    def save_all_stories(self) -> None:
        with open('stories.txt', 'w') as file:
            for story in self.stories:
                file.write(f"{story.username}|{story.title}|{story.content}\n")

    def get_all_stories(self) -> list:
        return self.stories

    def get_story_by_title(self, username: str, title: str) -> Story:
        for story in self.stories:
            if story.username == username and story.title == title:
                return story
        return None