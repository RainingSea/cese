class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        with open('stories.txt', 'a') as file:
            file.write(f"{self.username}|{self.title}|{self.content}\n")

class StoryManager:
    def create_story(self, username: str, title: str, content: str):
        story = Story(username, title, content)
        story.save()

    def edit_story(self, username: str, title: str, new_content: str) -> bool:
        with open('stories.txt', 'r') as file:
            stories = file.readlines()

        edited = False
        with open('stories.txt', 'w') as file:
            for line in stories:
                stored_username, stored_title, stored_content = line.strip().split('|')
                if stored_username == username and stored_title == title:
                    line = f"{username}|{title}|{new_content}\n"
                    edited = True
                file.write(line)

        return edited