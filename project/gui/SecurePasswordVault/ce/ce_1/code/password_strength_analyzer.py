class PasswordStrengthAnalyzer:
    def analyze(self, password: str) -> str:
        if len(password) < 6:
            return "Weak"
        elif len(password) < 10:
            return "Moderate"
        else:
            return "Strong"