from tkinter import Tk
from GUI import GUI
from ExpenseSplitter import ExpenseSplitter

def main():
    splitter = ExpenseSplitter()
    gui = GUI(splitter)
    gui.root.mainloop()

if __name__ == "__main__":
    main()