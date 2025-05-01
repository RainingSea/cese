import tkinter as tk
from tkinter import messagebox
from vault_manager import VaultManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Vault Manager")
        self.vault_manager = VaultManager()
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Create New Vault", command=self.create_vault).pack(pady=10)
        tk.Button(self.root, text="View Existing Vaults", command=self.view_vaults).pack(pady=10)

    def create_vault(self):
        vault_name = tk.simpledialog.askstring("Vault Name", "Enter the name of the vault:")
        if vault_name:
            self.vault_manager.create_vault(vault_name)
            messagebox.showinfo("Success", f"Vault '{vault_name}' created successfully!")

    def view_vaults(self):
        vaults = self.vault_manager.list_vaults()
        messagebox.showinfo("Existing Vaults", "\n".join(vaults) if vaults else "No vaults available.")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()