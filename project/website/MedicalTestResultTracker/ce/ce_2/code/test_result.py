class TestResult:
    def __init__(self, user_id: str, test_name: str, result: str, date: str):
        self.user_id = user_id
        self.test_name = test_name
        self.result = result
        self.date = date

    def save(self):
        with open('test_results.txt', 'a') as file:
            file.write(f"{self.user_id}|{self.test_name}|{self.result}|{self.date}\n")

    @staticmethod
    def load_results(user_id: str):
        results = []
        try:
            with open('test_results.txt', 'r') as file:
                for line in file:
                    data = line.strip().split('|')
                    if data[0] == user_id:
                        results.append(data[1:])  # Exclude user_id
        except FileNotFoundError:
            pass
        return results