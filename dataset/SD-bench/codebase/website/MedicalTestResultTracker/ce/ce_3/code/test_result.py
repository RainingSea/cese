class TestResult:
    def __init__(self, user_id: str, test_name: str, result: str, date: str):
        self.user_id = user_id
        self.test_name = test_name
        self.result = result
        self.date = date

    def save(self) -> None:
        with open('test_results.txt', 'a') as file:
            file.write(f"{self.user_id}|{self.test_name}|{self.result}|{self.date}\n")

    @classmethod
    def load_all(cls, user_id: str) -> list:
        test_results = []
        with open('test_results.txt', 'r') as file:
            for line in file:
                uid, test_name, result, date = line.strip().split('|')
                if uid == user_id:
                    test_results.append(cls(uid, test_name, result, date))
        return test_results