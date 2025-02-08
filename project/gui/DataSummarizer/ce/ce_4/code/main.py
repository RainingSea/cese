import tkinter as tk
from ui import UI

def main() -> str:
    """Main function to run the application."""
    root = tk.Tk()
    app = UI(root)
    root.mainloop()
    return "Application closed."

if __name__ == "__main__":
    main()