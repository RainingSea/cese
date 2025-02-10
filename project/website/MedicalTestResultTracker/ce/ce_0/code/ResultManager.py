class TestResult:
    def __init__(self, date: str, test_name: str, result: str):
        self.date = date
        self.test_name = test_name
        self.result = result

    def save(self):
        with open('results.txt', 'a') as f:
            f.write(f"{self.date}|{self.test_name}|{self.result}\n")

class ResultManager:
    def add_result(self, test_result: TestResult):
        test_result.save()

    def load_results(self) -> list:
        try:
            with open('results.txt', 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []