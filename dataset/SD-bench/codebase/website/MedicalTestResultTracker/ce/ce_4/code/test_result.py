class TestResult:
    def __init__(self, user_id: str, test_name: str, result_value: str, date: str):
        self.user_id = user_id
        self.test_name = test_name
        self.result_value = result_value
        self.date = date

    def save(self):
        with open('test_results.txt', 'a') as file:
            file.write(f'{self.user_id}|{self.test_name}|{self.result_value}|{self.date}\n')

    @staticmethod
    def load(user_id: str):
        results = []
        with open('test_results.txt', 'r') as file:
            for line in file:
                uid, test_name, result_value, date = line.strip().split('|')
                if uid == user_id:
                    results.append((test_name, result_value, date))
        return results