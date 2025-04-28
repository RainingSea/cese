class GroupManager:
    def __init__(self):
        self.groups = self.load_groups()

    def load_groups(self):
        groups = []
        with open('study_groups.txt', 'r') as f:
            for line in f:
                groups.append(line.strip())
        return groups

    def join_group(self, username: str, group_name: str) -> bool:
        if group_name in self.groups:
            # Logic to add user to the group (not implemented here)
            return True
        return False