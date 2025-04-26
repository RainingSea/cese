class TestResultManager:
    def __init__(self):
        self.test_results = self.load_test_results()

    def load_test_results(self):
        test_results = []
        try:
            with open('test_results.txt', 'r') as file:
                for line in file:
                    username, test_name, result, date = line.strip().split('|')
                    test_results.append((username, test_name, result, date))
        except FileNotFoundError:
            pass
        return test_results

    def add_test_result(self, username: str, test_name: str, result: str, date: str) -> None:
        self.test_results.append((username, test_name, result, date))
        with open('test_results.txt', 'a') as file:
            file.write(f"{username}|{test_name}|{result}|{date}\n")

    def get_test_results(self, username: str) -> list:
        return [result for result in self.test_results if result[0] == username]