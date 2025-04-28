class TestResultManager:
    def __init__(self, results_file: str):
        self.results_file = results_file
        self.results = self.load_results()

    def load_results(self) -> dict:
        results = {}
        try:
            with open(self.results_file, 'r') as file:
                for line in file:
                    username, result = line.strip().split('|')
                    if username not in results:
                        results[username] = []
                    results[username].append(result)
        except FileNotFoundError:
            pass  # If the file does not exist, return an empty dictionary
        return results

    def add_result(self, username: str, result: str) -> None:
        if username not in self.results:
            self.results[username] = []
        self.results[username].append(result)
        with open(self.results_file, 'a') as file:
            file.write(f"{username}|{result}\n")

    def get_results(self, username: str) -> list:
        return self.results.get(username, [])

    def get_trends(self, username: str) -> list:
        results = self.get_results(username)
        trends = []
        if results:
            trends.append(f"Total results: {len(results)}")
        return trends