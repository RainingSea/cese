class FileHandler:
    def write_to_file(self, filename: str, data: str) -> None:
        with open(filename, 'a') as f:
            f.write(data + '\n')

    def read_from_file(self, filename: str) -> list:
        with open(filename, 'r') as f:
            return f.read().strip().split('\n')