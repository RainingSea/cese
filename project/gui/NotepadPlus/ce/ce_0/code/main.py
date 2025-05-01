import tkinter as tk
from text_editor import TextEditor

class Main:
    def main(self) -> str:
        root = tk.Tk()
        root.title("Simple Text Editor")
        text_editor = TextEditor(root)
        root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()