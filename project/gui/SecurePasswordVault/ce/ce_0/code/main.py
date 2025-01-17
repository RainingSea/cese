import tkinter as tk
from tkinter import messagebox
from vault_manager import VaultManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Vault")
        self.vault_manager = VaultManager()
        self.create_widgets()

    def create_widgets(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.vault_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Vaults", menu=self.vault_menu)
        self.vault_menu.add_command(label="Create Vault", command=self.create_vault)
        self.vault_menu.add_command(label="Add Password", command=self.add_password)
        self.vault_menu.add_command(label="Search Password", command=self.search_password)

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.update_vault_list()

    def update_vault_list(self):
        self.listbox.delete(0, tk.END)
        for vault_name in self.vault_manager.vaults.keys():
            self.listbox.insert(tk.END, vault_name)

    def create_vault(self):
        vault_name = tk.simpledialog.askstring("Vault Name", "Enter the vault name:")
        if vault_name and self.vault_manager.create_vault(vault_name):
            self.update_vault_list()
        else:
            messagebox.showerror("Error", "Vault already exists or invalid name.")

    def add_password(self):
        vault_name = self.listbox.get(tk.ACTIVE)
        if not vault_name:
            messagebox.showwarning("Warning", "Select a vault first.")
            return

        website = tk.simpledialog.askstring("Website", "Enter the website:")
        username = tk.simpledialog.askstring("Username", "Enter the username:")
        password = tk.simpledialog.askstring("Password", "Enter the password:")
        
        if self.vault_manager.add_password(vault_name, website, username, password):
            messagebox.showinfo("Success", "Password added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add password.")

    def search_password(self):
        vault_name = self.listbox.get(tk.ACTIVE)
        if not vault_name:
            messagebox.showwarning("Warning", "Select a vault first.")
            return

        query = tk.simpledialog.askstring("Search", "Enter search query:")
        results = self.vault_manager.search_password(vault_name, query)
        if results:
            result_str = "\n".join([f"{entry['website']} | {entry['username']}" for entry in results])
            messagebox.showinfo("Search Results", result_str)
        else:
            messagebox.showinfo("Search Results", "No results found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()