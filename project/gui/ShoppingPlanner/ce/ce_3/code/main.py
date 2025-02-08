from shopping_list_manager import ShoppingListManager

def main() -> str:
    shopping_list_manager = ShoppingListManager()
    shopping_list_manager.load_lists()
    return "Shopping Planner Initialized"

if __name__ == "__main__":
    print(main())