from ui import UI
from notebook_manager import NotebookManager

def main() -> None:
    notebook_manager = NotebookManager()
    ui = UI(notebook_manager)

if __name__ == "__main__":
    main()