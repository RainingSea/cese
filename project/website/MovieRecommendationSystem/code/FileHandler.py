import os
import fcntl

class FileHandler:
    def __init__(self):
        pass

    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                fcntl.flock(file, fcntl.LOCK_SH)
                try:
                    return [line.strip() for line in file.readlines() if line.strip()]
                finally:
                    fcntl.flock(file, fcntl.LOCK_UN)
        except FileNotFoundError:
            return []

    def write_file(self, filename, data):
        with open(filename, 'w') as file:
            fcntl.flock(file, fcntl.LOCK_EX)
            try:
                for line in data:
                    file.write(line + '\n')
            finally:
                fcntl.flock(file, fcntl.LOCK_UN)

    def validate_file(self, filename):
        return os.path.exists(filename)