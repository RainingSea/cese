class GroupManager:
    def __init__(self):
        self.groups = []

    def join_group(self, username: str, group_name: str) -> None:
        if group_name not in self.groups:
            self.groups.append(group_name)
            self.save_groups()

    def load_groups(self) -> list:
        try:
            with open('groups.txt', 'r') as file:
                self.groups = [line.strip() for line in file]
        except FileNotFoundError:
            self.groups = []

    def save_groups(self) -> None:
        with open('groups.txt', 'w') as file:
            for group in self.groups:
                file.write(f"{group}\n")