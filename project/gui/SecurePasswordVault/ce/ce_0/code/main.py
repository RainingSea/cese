import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

class Main:
    def __init__(self):
        self.vault_manager = VaultManager()

    def main(self):
        self.vault_manager.load_vaults()
        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Password Vault")

        self.vault_label = tk.Label(self.root, text="Select Vault:")
        self.vault_label.pack()

        self.vault_listbox = tk.Listbox(self.root)
        self.vault_listbox.pack()

        self.add_vault_button = tk.Button(self.root, text="Add Vault", command=self.add_vault)
        self.add_vault_button.pack()

        self.password_frame = tk.Frame(self.root)
        self.password_frame.pack()

        self.password_label = tk.Label(self.password_frame, text="Password:")
        self.password_label.grid(row=0, column=0)

        self.password_entry = tk.Entry(self.password_frame)
        self.password_entry.grid(row=0, column=1)

        self.add_password_button = tk.Button(self.root, text="Add Password", command=self.add_password)
        self.add_password_button.pack()

        self.root.mainloop()

    def add_vault(self):
        vault_name = tk.simpledialog.askstring("Vault Name", "Enter the name of the vault:")
        if vault_name:
            self.vault_manager.create_vault(vault_name)
            self.update_vault_list()

    def add_password(self):
        vault_name = self.vault_listbox.get(tk.ACTIVE)
        password = self.password_entry.get()
        if vault_name and password:
            self.vault_manager.add_password(vault_name, password)
            self.password_entry.delete(0, tk.END)

    def update_vault_list(self):
        self.vault_listbox.delete(0, tk.END)
        for vault in self.vault_manager.vaults:
            self.vault_listbox.insert(tk.END, vault)

class VaultManager:
    def __init__(self):
        self.vaults = []

    def load_vaults(self):
        if os.path.exists("vaults.txt"):
            with open("vaults.txt", "r") as file:
                self.vaults = [line.strip() for line in file.readlines()]

    def create_vault(self, name: str) -> None:
        if name not in self.vaults:
            self.vaults.append(name)
            with open("vaults.txt", "a") as file:
                file.write(name + "\n")
            with open(f"{name}.txt", "w") as file:
                file.write("")  # Create an empty vault file

    def add_password(self, vault_name: str, password: str) -> None:
        encrypted_password = PasswordEncryption.encrypt(password)
        with open(f"{vault_name}.txt", "a") as file:
            file.write(encrypted_password + "\n")

class PasswordEncryption:
    @staticmethod
    def encrypt(password: str) -> str:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_password = cipher.encrypt(password.encode())
        return encrypted_password.decode()

    @staticmethod
    def decrypt(encrypted_password: str) -> str:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        decrypted_password = cipher.decrypt(encrypted_password.encode())
        return decrypted_password.decode()

if __name__ == "__main__":
    app = Main()
    app.main()