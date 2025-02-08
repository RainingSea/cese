class ReportGenerator:
    def generate_report(self) -> str:
        report = "Task Report:\n"
        try:
            with open('timers.txt', 'r') as file:
                for line in file:
                    task_title, duration, start_time = line.strip().split('|')
                    report += f"Task: {task_title}, Duration: {duration} seconds\n"
        except FileNotFoundError:
            report += "No timers recorded."
        self.save_reports(report)
        return report

    def load_reports(self) -> None:
        try:
            with open('reports.txt', 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "No reports available."

    def save_reports(self, report: str) -> None:
        with open('reports.txt', 'w') as file:
            file.write(report)