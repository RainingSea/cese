from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.product_manager = ProductManager()
        self.cart_manager = CartManager()

    def main(self):
        app.run(port=8206, debug=False)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as file:
            users = {}
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
            return users

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class ProductManager:
    def __init__(self):
        self.products = self.load_products()

    def load_products(self) -> list:
        if not os.path.exists('products.txt'):
            return []
        with open('products.txt', 'r') as file:
            products = []
            for line in file:
                product_id, name, price = line.strip().split('|')
                products.append({'id': product_id, 'name': name, 'price': float(price)})
            return products

    def get_product(self, product_id: str) -> dict:
        for product in self.products:
            if product['id'] == product_id:
                return product
        return {}

class CartManager:
    def __init__(self):
        self.cart = self.load_cart()

    def load_cart(self) -> dict:
        if not os.path.exists('cart.txt'):
            return {}
        with open('cart.txt', 'r') as file:
            cart = {}
            for line in file:
                product_id, quantity = line.strip().split('|')
                cart[product_id] = int(quantity)
            return cart

    def add_to_cart(self, product_id: str, quantity: int) -> None:
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.save_cart()

    def remove_from_cart(self, product_id: str) -> None:
        if product_id in self.cart:
            del self.cart[product_id]
            self.save_cart()

    def view_cart(self) -> dict:
        return self.cart

    def save_cart(self) -> None:
        with open('cart.txt', 'w') as file:
            for product_id, quantity in self.cart.items():
                file.write(f"{product_id}|{quantity}\n")

class Order:
    def __init__(self, items: dict, shipping_address: str, payment_info: str):
        self.items = items
        self.shipping_address = shipping_address
        self.payment_info = payment_info

    def confirm_order(self) -> bool:
        # Here you would handle order confirmation logic
        return True

@app.route('/')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    main_app = Main()
    main_app.main()