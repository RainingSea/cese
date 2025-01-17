class CalculationLogger:
    def log_to_file(self, file_name: str, operation: str, result: float) -> None:
        with open(file_name, 'a') as file:
            file.write(f"{operation}|{result}\n")