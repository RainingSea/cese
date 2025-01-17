import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt
from investment import Investment
from goal import Goal

class InvestmentTracker:
    def __init__(self):
        self.investments = []
        self.goals = []
        self.load_data()

    def add_investment(self, type: str, amount: float, category: str, date: str):
        investment = Investment(type, amount, category, date)
        self.investments.append(investment)
        self.save_data()

    def set_goal(self, goal_name: str, amount: float, deadline: str):
        goal = Goal(goal_name, amount, deadline)
        self.goals.append(goal)
        self.save_data()

    def generate_report(self) -> str:
        report = "Investment Report:\n"
        for investment in self.investments:
            report += f"{investment.type} | {investment.amount} | {investment.category} | {investment.date}\n"
        return report

    def visualize_performance(self):
        categories = [inv.category for inv in self.investments]
        amounts = [inv.amount for inv in self.investments]
        plt.bar(categories, amounts)
        plt.title('Investment Performance')
        plt.xlabel('Categories')
        plt.ylabel('Amount')
        plt.show()

    def load_data(self):
        try:
            with open('investments.txt', 'r') as f:
                for line in f:
                    type, amount, category, date = line.strip().split(',')
                    self.add_investment(type, float(amount), category, date)
            with open('goals.txt', 'r') as f:
                for line in f:
                    goal_name, amount, deadline = line.strip().split(',')
                    self.set_goal(goal_name, float(amount), deadline)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('investments.txt', 'w') as f:
            for investment in self.investments:
                f.write(f"{investment.type},{investment.amount},{investment.category},{investment.date}\n")
        with open('goals.txt', 'w') as f:
            for goal in self.goals:
                f.write(f"{goal.goal_name},{goal.amount},{goal.deadline}\n")

def main():
    tracker = InvestmentTracker()

    # GUI setup
    root = tk.Tk()
    root.title("Investment Tracker")

    def add_investment():
        type = entry_type.get()
        amount = entry_amount.get()
        category = entry_category.get()
        date = entry_date.get()
        tracker.add_investment(type, float(amount), category, date)
        messagebox.showinfo("Success", "Investment added!")

    def set_goal():
        goal_name = entry_goal_name.get()
        amount = entry_goal_amount.get()
        deadline = entry_goal_deadline.get()
        tracker.set_goal(goal_name, float(amount), deadline)
        messagebox.showinfo("Success", "Goal set!")

    def show_report():
        report = tracker.generate_report()
        messagebox.showinfo("Report", report)

    def visualize():
        tracker.visualize_performance()

    # Input fields
    tk.Label(root, text="Type").pack()
    entry_type = tk.Entry(root)
    entry_type.pack()

    tk.Label(root, text="Amount").pack()
    entry_amount = tk.Entry(root)
    entry_amount.pack()

    tk.Label(root, text="Category").pack()
    entry_category = tk.Entry(root)
    entry_category.pack()

    tk.Label(root, text="Date").pack()
    entry_date = tk.Entry(root)
    entry_date.pack()

    tk.Button(root, text="Add Investment", command=add_investment).pack()

    tk.Label(root, text="Goal Name").pack()
    entry_goal_name = tk.Entry(root)
    entry_goal_name.pack()

    tk.Label(root, text="Goal Amount").pack()
    entry_goal_amount = tk.Entry(root)
    entry_goal_amount.pack()

    tk.Label(root, text="Goal Deadline").pack()
    entry_goal_deadline = tk.Entry(root)
    entry_goal_deadline.pack()

    tk.Button(root, text="Set Goal", command=set_goal).pack()
    tk.Button(root, text="Show Report", command=show_report).pack()
    tk.Button(root, text="Visualize Performance", command=visualize).pack()

    root.mainloop()

if __name__ == "__main__":
    main()