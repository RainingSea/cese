class FileManager:
    def read_file(self, filename: str) -> list:
        try:
            with open(filename, 'r') as file:
                return file.read().strip().split('\n')
        except FileNotFoundError:
            return []

    def write_file(self, filename: str, data: list) -> None:
        with open(filename, 'w') as file:
            file.write('\n'.join(data))