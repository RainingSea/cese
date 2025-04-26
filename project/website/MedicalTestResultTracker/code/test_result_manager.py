class TestResultManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.results = self.load_test_results()

    def add_test_result(self, username: str, result: str) -> bool:
        if username is None:
            return False
        self.results.append(f"{username}|{result}")
        self.save_test_results()
        return True

    def get_test_results(self, username: str) -> list:
        if username is None:
            return []
        return [result.split('|')[1] for result in self.results if result.startswith(username)]

    def load_test_results(self) -> list:
        try:
            with open(self.filename, 'r') as file:
                return file.read().strip().split('\n')
        except FileNotFoundError:
            return []

    def save_test_results(self):
        with open(self.filename, 'w') as file:
            file.write('\n'.join(self.results))