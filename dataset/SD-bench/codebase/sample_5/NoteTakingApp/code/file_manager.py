class FileManager:
    def read_file(self, file_path: str) -> list[str]:
        """Read a file and return its contents as a list of lines."""
        with open(file_path, 'r') as f:
            return f.readlines()

    def write_file(self, file_path: str, data: list[str]):
        """Write a list of strings to a file."""
        with open(file_path, 'w') as f:
            f.writelines("\n".join(data) + "\n")