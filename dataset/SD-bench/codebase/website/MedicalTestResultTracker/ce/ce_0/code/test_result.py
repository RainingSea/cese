class TestResult:
    def __init__(self, user: str, test_name: str, result: float, date: str):
        self.user = user
        self.test_name = test_name
        self.result = result
        self.date = date

    def save_to_file(self, filename: str):
        with open(filename, 'a') as file:
            file.write(f"{self.user}|{self.test_name}|{self.result}|{self.date}\n")

    @staticmethod
    def load_from_file(filename: str) -> list:
        results = []
        with open(filename, 'r') as file:
            for line in file:
                user, test_name, result, date = line.strip().split('|')
                results.append(TestResult(user, test_name, float(result), date))
        return results