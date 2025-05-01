class Puzzle:
    def __init__(self, rule: str, solution: str, hint: str):
        self.rule = rule
        self.solution = solution
        self.hint = hint

    def check_solution(self, answer: str) -> bool:
        return answer.lower() == self.solution.lower()