class GroupManager:
    def __init__(self):
        self.groups = self.load_groups()

    def load_groups(self):
        groups = {}
        with open('groups.txt', 'r') as file:
            for line in file:
                name, interests = line.strip().split('|')
                groups[name] = interests.split(',')
        return groups

    def create_group(self, name: str, interests: list) -> bool:
        if name in self.groups:
            return False
        self.groups[name] = interests
        self.save_groups()
        return True

    def join_group(self, username: str, group_name: str) -> bool:
        # Logic to join a group
        return True

    def get_groups(self):
        return self.groups.keys()

    def save_groups(self):
        with open('groups.txt', 'w') as file:
            for name, interests in self.groups.items():
                file.write(f"{name}|{','.join(interests)}\n")