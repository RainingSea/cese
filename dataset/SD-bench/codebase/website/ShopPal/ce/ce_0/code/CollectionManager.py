class CollectionManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_collection(self, username: str, products: list) -> bool:
        with open(self.file_path, 'a') as file:
            file.write(f"{username}|{','.join(products)}\n")
        return True

    def load_collection(self, username: str) -> list:
        collections = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    user, products = line.strip().split('|')
                    if user == username:
                        collections = products.split(',')
                        break
        except FileNotFoundError:
            pass
        return collections