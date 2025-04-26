class AdviceManager:
    def __init__(self):
        self.advice_posts = self.load_advice()

    def load_advice(self):
        advice_posts = []
        try:
            with open('advice.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    advice_posts.append({'title': title, 'content': content})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return advice_posts

    def post_advice(self, title: str, content: str) -> bool:
        self.advice_posts.append({'title': title, 'content': content})
        self.save_advice()
        return True

    def get_advice(self) -> list:
        return self.advice_posts

    def save_advice(self):
        with open('advice.txt', 'w') as file:
            for advice in self.advice_posts:
                file.write(f"{advice['title']}|{advice['content']}\n")