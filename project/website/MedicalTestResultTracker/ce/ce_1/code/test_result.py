class TestResult:
    def __init__(self):
        self.results_file_template = 'results_{}.txt'

    def add_result(self, username: str, date: str, result: float) -> None:
        results_file = self.results_file_template.format(username)
        with open(results_file, 'a') as file:
            file.write(f"{date}|{result}\n")

    def get_results(self, username: str) -> list:
        results_file = self.results_file_template.format(username)
        results = []
        if os.path.exists(results_file):
            with open(results_file, 'r') as file:
                for line in file:
                    date, result = line.strip().split('|')
                    results.append((date, float(result)))
        return results