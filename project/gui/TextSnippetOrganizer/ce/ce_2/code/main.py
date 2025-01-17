import tkinter as tk
from snippets.gui import GUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Snippet Manager")
    app = GUI(root)
    root.mainloop()