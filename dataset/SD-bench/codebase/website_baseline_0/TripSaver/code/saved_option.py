class SavedOption:
    def __init__(self, user: str, options: list):
        self.user = user
        self.options = options

    def save(self) -> None:
        with open('saved_options.txt', 'a') as f:
            f.write(f"{self.user}|{','.join(self.options)}\n")