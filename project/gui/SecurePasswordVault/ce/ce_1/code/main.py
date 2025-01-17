import tkinter as tk
from tkinter import messagebox
from vault_manager import VaultManager

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Vault")
        self.vault_manager = VaultManager()
        self.create_widgets()

    def create_widgets(self):
        self.vault_listbox = tk.Listbox(self.root)
        self.vault_listbox.pack(fill=tk.BOTH, expand=True)

        self.add_vault_button = tk.Button(self.root, text="Create Vault", command=self.create_vault)
        self.add_vault_button.pack()

        self.load_vaults()

    def create_vault(self):
        vault_name = tk.simpledialog.askstring("Vault Name", "Enter vault name:")
        if vault_name:
            self.vault_manager.create_vault(vault_name)
            self.load_vaults()

    def load_vaults(self):
        self.vault_listbox.delete(0, tk.END)
        for vault in self.vault_manager.vaults.keys():
            self.vault_listbox.insert(tk.END, vault)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()