class FileHandler:
    def read_file(self, file_path: str) -> list:
        """Read lines from a file and return them as a list."""
        with open(file_path, 'r') as file:
            return file.readlines()

    def write_file(self, file_path: str, data: list):
        """Write a list of strings to a file."""
        with open(file_path, 'w') as file:
            file.writelines(data)

    def append_to_file(self, file_path: str, line: str):
        """Append a line to a file."""
        with open(file_path, 'a') as file:
            file.write(line + '\n')