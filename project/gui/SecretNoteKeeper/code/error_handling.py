class ErrorHandling:
    @staticmethod
    def handle_file_error(error: Exception) -> None:
        print(f"File error: {error}")

    @staticmethod
    def validate_user_input(input_data: str) -> bool:
        return bool(input_data.strip())