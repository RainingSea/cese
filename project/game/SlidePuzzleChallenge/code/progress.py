class Progress:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data: str):
        with open(self.file_path, 'w') as file:
            file.write(data)

    def load(self) -> str:
        with open(self.file_path, 'r') as file:
            return file.read()