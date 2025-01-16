class TestResult:
    def __init__(self, user: str, test_name: str, result: float, date: str):
        self.user = user
        self.test_name = test_name
        self.result = result
        self.date = date

    def save(self):
        with open('test_results.txt', 'a') as file:
            file.write(f"{self.user}|{self.test_name}|{self.result}|{self.date}\n")

    @staticmethod
    def load(user: str):
        results = []
        with open('test_results.txt', 'r') as file:
            for line in file:
                test_user, test_name, result, date = line.strip().split('|')
                if test_user == user:
                    results.append(TestResult(test_user, test_name, float(result), date))
        return results