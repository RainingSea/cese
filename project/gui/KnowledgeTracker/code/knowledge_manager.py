import os
from data_storage import handle_file_io_errors

class KnowledgeManager:
    def __init__(self):
        self.theories_file = "theories.txt"
        self.concepts_file = "concepts.txt"
        self.experiments_file = "experiments.txt"
        self.ensure_files_exist()

    def ensure_files_exist(self):
        for file in [self.theories_file, self.concepts_file, self.experiments_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    pass

    def load_entries(self, category: str) -> list:
        file_map = {
            "theories": self.theories_file,
            "concepts": self.concepts_file,
            "experiments": self.experiments_file
        }
        entries = []
        try:
            with open(file_map[category], 'r') as f:
                entries = f.readlines()
            return [entry.strip() for entry in entries]
        except Exception as e:
            handle_file_io_errors(e)
            return []

    def save_entry(self, entry: str, category: str):
        self.validate_category(category)
        file_map = {
            "theories": self.theories_file,
            "concepts": self.concepts_file,
            "experiments": self.experiments_file
        }
        try:
            with open(file_map[category], 'a') as f:
                f.write(f"{entry}\n")
        except Exception as e:
            handle_file_io_errors(e)

    def update_entry(self, old_entry: str, new_entry: str, category: str):
        self.validate_category(category)
        entries = self.load_entries(category)
        entries = [new_entry if entry.strip() == old_entry else entry for entry in entries]
        self.save_all_entries(entries, category)

    def delete_entry(self, entry: str, category: str):
        self.validate_category(category)
        entries = self.load_entries(category)
        entries = [e for e in entries if e.strip() != entry]
        self.save_all_entries(entries, category)

    def save_all_entries(self, entries: list, category: str):
        self.validate_category(category)
        file_map = {
            "theories": self.theories_file,
            "concepts": self.concepts_file,
            "experiments": self.experiments_file
        }
        try:
            with open(file_map[category], 'w') as f:
                for entry in entries:
                    f.write(f"{entry}\n")
        except Exception as e:
            handle_file_io_errors(e)

    def validate_category(self, category: str):
        if category not in ['theories', 'concepts', 'experiments']:
            raise ValueError("Invalid type specified.")