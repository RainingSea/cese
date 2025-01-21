class TestResult:
    def __init__(self, user_id: str, test_name: str, result: str, date: str):
        self.user_id = user_id
        self.test_name = test_name
        self.result = result
        self.date = date

    def save(self):
        with open('results.txt', 'a') as file:
            file.write(f"{self.user_id}|{self.test_name}|{self.result}|{self.date}\n")

    @staticmethod
    def load(user_id: str):
        results = []
        with open('results.txt', 'r') as file:
            for line in file:
                result_data = line.strip().split('|')
                if result_data[0] == user_id:
                    results.append(TestResult(result_data[0], result_data[1], result_data[2], result_data[3]))
        return results