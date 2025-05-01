import tkinter as tk
from tkinter import messagebox, simpledialog
from vault import VaultManager
from user import UserManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Vault Manager")
        self.vault_manager = VaultManager()
        self.user_manager = UserManager()
        self.create_widgets()

    def create_widgets(self):
        self.login_frame = tk.Frame(self.master)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.login_user(username, password):
            messagebox.showinfo("Login", "Login successful!")
            self.login_frame.pack_forget()
            self.show_vaults()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def show_vaults(self):
        self.vault_frame = tk.Frame(self.master)
        self.vault_frame.pack()

        tk.Label(self.vault_frame, text="Select Vault:").pack()
        self.vault_listbox = tk.Listbox(self.vault_frame)
        self.vault_listbox.pack()

        tk.Button(self.vault_frame, text="Add Vault", command=self.add_vault).pack()
        tk.Button(self.vault_frame, text="Add Password", command=self.add_password).pack()
        tk.Button(self.vault_frame, text="Edit Password", command=self.edit_password).pack()
        tk.Button(self.vault_frame, text="Delete Password", command=self.delete_password).pack()
        tk.Button(self.vault_frame, text="Search Password", command=self.search_password).pack()

        self.update_vault_list()

    def add_vault(self):
        vault_name = simpledialog.askstring("Vault Name", "Enter the name of the vault:")
        if vault_name:
            try:
                self.vault_manager.create_vault(vault_name)
                self.update_vault_list()
                messagebox.showinfo("Vault", f"Vault '{vault_name}' created successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def add_password(self):
        vault_name = self.vault_listbox.get(tk.ACTIVE)
        password = simpledialog.askstring("Password", "Enter the password:")
        if vault_name and password:
            try:
                self.vault_manager.add_password(vault_name, password)
                messagebox.showinfo("Password", "Password added successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def edit_password(self):
        vault_name = self.vault_listbox.get(tk.ACTIVE)
        old_password = simpledialog.askstring("Edit Password", "Enter the password to edit:")
        new_password = simpledialog.askstring("New Password", "Enter the new password:")
        if vault_name and old_password and new_password:
            try:
                self.vault_manager.edit_password(vault_name, old_password, new_password)
                messagebox.showinfo("Password", "Password edited successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def delete_password(self):
        vault_name = self.vault_listbox.get(tk.ACTIVE)
        password = simpledialog.askstring("Delete Password", "Enter the password to delete:")
        if vault_name and password:
            try:
                self.vault_manager.delete_password(vault_name, password)
                messagebox.showinfo("Password", "Password deleted successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def search_password(self):
        vault_name = self.vault_listbox.get(tk.ACTIVE)
        query = simpledialog.askstring("Search Password", "Enter the password to search:")
        if vault_name and query:
            result = self.vault_manager.search_password(vault_name, query)
            messagebox.showinfo("Search Result", result)

    def update_vault_list(self):
        self.vault_listbox.delete(0, tk.END)
        for vault in self.vault_manager.list_vaults():
            self.vault_listbox.insert(tk.END, vault)

    def main(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()