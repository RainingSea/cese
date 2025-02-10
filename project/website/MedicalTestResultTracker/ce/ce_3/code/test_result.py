class TestResult:
    def __init__(self, test_name: str, result_value: float, date: str):
        self.test_name = test_name
        self.result_value = result_value
        self.date = date

    def save(self, username: str) -> None:
        with open(f'results_{username}.txt', 'a') as f:
            f.write(f"{self.test_name}|{self.result_value}|{self.date}\n")

    @staticmethod
    def load_history(username: str) -> list:
        results = []
        try:
            with open(f'results_{username}.txt', 'r') as f:
                for line in f:
                    result_data = line.strip().split('|')
                    results.append({
                        'test_name': result_data[0],
                        'result_value': float(result_data[1]),
                        'date': result_data[2]
                    })
        except FileNotFoundError:
            return results
        return results