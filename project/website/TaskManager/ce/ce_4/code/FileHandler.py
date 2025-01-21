class FileHandler:
    def write_to_file(self, filename: str, data: str):
        with open(filename, 'a') as file:
            file.write(data + '\n')

    def read_from_file(self, filename: str) -> list:
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []