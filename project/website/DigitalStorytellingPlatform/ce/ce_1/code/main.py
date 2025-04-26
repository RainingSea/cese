import os

class Main:
    def main(self):
        # Load user data
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users[username] = (password, email)
        return users

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username][0] == password:
            return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password},{email}\n")
        self.users[username] = (password, email)
        return True

    def create_story(self, username: str, title: str, content: str) -> bool:
        filename = f"{username}_stories.txt"
        with open(filename, 'a') as file:
            file.write(f"{title}|{content}\n")
        return True

    def edit_story(self, username: str, title: str, new_content: str) -> bool:
        filename = f"{username}_stories.txt"
        if not os.path.exists(filename):
            return False
        
        stories = []
        found = False
        with open(filename, 'r') as file:
            for line in file:
                story_title, content = line.strip().split('|')
                if story_title == title:
                    stories.append(f"{title}|{new_content}\n")
                    found = True
                else:
                    stories.append(line)
        
        if found:
            with open(filename, 'w') as file:
                file.writelines(stories)
            return True
        return False

main_app = Main()
main_app.main()