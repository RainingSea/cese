class StudyGroup:
    def __init__(self, group_name: str):
        self.group_name = group_name
        self.members = []

    def create_group(self):
        """Save the study group to the study_groups.txt file."""
        with open('study_groups.txt', 'a') as file:
            file.write(f"{self.group_name}|{','.join(self.members)}\n")

    def join_group(self, username: str):
        """Add a user to the study group."""
        if username not in self.members:
            self.members.append(username)

    @staticmethod
    def load_groups() -> list:
        """Load study groups from the study_groups.txt file."""
        groups = []
        try:
            with open('study_groups.txt', 'r') as file:
                for line in file:
                    group_name, members = line.strip().split('|')
                    groups.append({'group_name': group_name, 'members': members.split(',')})
        except FileNotFoundError:
            return []
        return groups