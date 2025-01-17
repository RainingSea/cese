from ExpenseSplitter import ExpenseSplitter
from GUI import GUI

if __name__ == "__main__":
    expense_splitter = ExpenseSplitter()
    gui = GUI(expense_splitter)
    gui.run()