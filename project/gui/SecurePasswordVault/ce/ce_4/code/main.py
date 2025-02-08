import tkinter as tk
from vault_manager import VaultManager

class Main:
    def __init__(self) -> None:
        self.vault_manager = VaultManager()
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self) -> None:
        # Create main menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        vault_menu = tk.Menu(menu)
        menu.add_cascade(label="Vaults", menu=vault_menu)
        vault_menu.add_command(label="Create Vault", command=self.create_vault)

        # Add more menu options as needed

    def create_vault(self) -> None:
        vault_name = "new_vault"  # Replace with user input
        self.vault_manager.create_vault(vault_name)

if __name__ == "__main__":
    main = Main()