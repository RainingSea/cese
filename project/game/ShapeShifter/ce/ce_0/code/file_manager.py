import os

class FileManager:
    def load_shapes(self, file_path: str) -> list:
        shapes = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                shapes = [line.strip() for line in file.readlines()]
        return shapes

    def load_target_patterns(self, file_path: str) -> tuple:
        target_patterns = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file.readlines():
                    shape_info = line.strip().split('|')
                    target_patterns.append(tuple(shape_info))
        return target_patterns