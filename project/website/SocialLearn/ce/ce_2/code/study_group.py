class StudyGroup:
    """StudyGroup class to handle study group operations."""
    def __init__(self, name: str):
        self.name = name
        self.members = []

    def join_group(self, username: str) -> bool:
        """Add a user to the study group."""
        self.members.append(username)
        try:
            with open('study_groups.txt', 'a') as file:
                file.write(f"{self.name}|{username}\n")
            return True
        except Exception as e:
            print(f"Error joining group: {e}")
            return False

    def get_members(self) -> list:
        """Retrieve all members of the study group."""
        members = []
        try:
            with open('study_groups.txt', 'r') as file:
                for line in file:
                    group_name, member = line.strip().split('|')
                    if group_name == self.name:
                        members.append(member)
        except Exception as e:
            print(f"Error loading group members: {e}")
        return members