from user_interface import UserInterface
from shopping_planner import ShoppingPlanner

def main():
    planner = ShoppingPlanner()
    ui = UserInterface(planner)
    ui.root.mainloop()

if __name__ == "__main__":
    main()