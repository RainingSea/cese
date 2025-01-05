class Story:
    def __init__(self, title: str, content: str, user_id: str):
        self.title = title
        self.content = content
        self.user_id = user_id

    def save(self):
        with open('stories.txt', 'a') as f:
            f.write(f"{self.user_id}|{self.title}|{self.content}\n")

    @staticmethod
    def load(user_id: str):
        stories = []
        with open('stories.txt', 'r') as f:
            for line in f:
                story_data = line.strip().split('|')
                if story_data[0] == user_id:
                    stories.append(Story(story_data[1], story_data[2], story_data[0]))
        return stories