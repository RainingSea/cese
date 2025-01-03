class FileManager:
    def read_file(self, filename: str) -> list:
        with open(filename, 'r') as file:
            return file.readlines()

    def write_file(self, filename: str, data: list):
        with open(filename, 'w') as file:
            file.writelines(data)