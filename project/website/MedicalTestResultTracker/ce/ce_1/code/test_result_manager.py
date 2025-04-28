class TestResultManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_test_results()

    def load_test_results(self):
        self.test_results = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, test_name, date, result = line.strip().split(',')
                    if username not in self.test_results:
                        self.test_results[username] = []
                    self.test_results[username].append({
                        'test_name': test_name,
                        'date': date,
                        'result': result
                    })
        except FileNotFoundError:
            pass

    def add_test_result(self, username: str, test_name: str, date: str, result: str) -> None:
        if username not in self.test_results:
            self.test_results[username] = []
        self.test_results[username].append({
            'test_name': test_name,
            'date': date,
            'result': result
        })
        with open(self.filename, 'a') as file:
            file.write(f"{username},{test_name},{date},{result}\n")

    def get_test_results(self, username: str) -> list:
        return self.test_results.get(username, [])

    def get_trends(self, username: str) -> dict:
        trends = {}
        for entry in self.test_results.get(username, []):
            test_name = entry['test_name']
            if test_name not in trends:
                trends[test_name] = []
            trends[test_name].append((entry['date'], entry['result']))
        return trends