import tkinter as tk
from tkinter import messagebox
from vault_manager import VaultManager

class Main:
    def __init__(self) -> None:
        self.vault_manager = VaultManager()
        self.root = tk.Tk()
        self.root.title("Secure Password Vault")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self) -> None:
        self.vault_listbox = tk.Listbox(self.root)
        self.vault_listbox.pack()
        self.load_vaults()

        self.add_vault_button = tk.Button(self.root, text="Add Vault", command=self.add_vault)
        self.add_vault_button.pack()

    def load_vaults(self) -> None:
        for vault in self.vault_manager.vaults.keys():
            self.vault_listbox.insert(tk.END, vault)

    def add_vault(self) -> None:
        vault_name = tk.simpledialog.askstring("Vault Name", "Enter the name of the vault:")
        if vault_name and self.vault_manager.create_vault(vault_name):
            self.load_vaults()
        else:
            messagebox.showerror("Error", "Vault already exists or invalid name.")

if __name__ == "__main__":
    Main()