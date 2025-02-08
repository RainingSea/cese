from ui import UI
from notebooks import Notebooks

class Main:
    def __init__(self) -> None:
        self.notebooks = Notebooks()
        self.ui = UI(self)

    def main(self) -> str:
        return "Notebook Application Started"

if __name__ == "__main__":
    app = Main()
    app.main()