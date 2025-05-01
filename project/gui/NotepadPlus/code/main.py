import tkinter as tk
from text_editor import TextEditor

class Main:
    def main(self) -> str:
        root = tk.Tk()
        root.title("Notepad Plus")
        text_editor = TextEditor(root)
        root.mainloop()
        return "Application closed."

if __name__ == "__main__":
    app = Main()
    app.main()