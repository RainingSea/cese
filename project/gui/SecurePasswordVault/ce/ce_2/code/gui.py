import tkinter as tk
from tkinter import messagebox
from vault_manager import VaultManager
from password import Password

class AppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Vault")
        self.vault_manager = VaultManager()
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.vault_name_entry = tk.Entry(self.main_frame)
        self.vault_name_entry.pack()

        self.add_vault_button = tk.Button(self.main_frame, text="Add Vault", command=self.add_vault)
        self.add_vault_button.pack()

        self.account_name_entry = tk.Entry(self.main_frame)
        self.account_name_entry.pack()

        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack()

        self.notes_entry = tk.Entry(self.main_frame)
        self.notes_entry.pack()

        self.add_password_button = tk.Button(self.main_frame, text="Add Password", command=self.add_password)
        self.add_password_button.pack()

    def add_vault(self):
        vault_name = self.vault_name_entry.get()
        if vault_name:
            self.vault_manager.create_vault(vault_name)
            messagebox.showinfo("Success", f"Vault '{vault_name}' created!")

    def add_password(self):
        account_name = self.account_name_entry.get()
        password = self.password_entry.get()
        notes = self.notes_entry.get()
        if account_name and password:
            new_password = Password(account_name, password, notes)
            self.vault_manager.add_password(self.vault_name_entry.get(), new_password)
            messagebox.showinfo("Success", "Password added!")