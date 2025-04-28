[CONTENT]
"Required packages": [
    "os", 
    "json"
],

"Required Other language third-party packages": [],

"Logic Analysis": {
    "main.py": {
        "classes": [
            {
                "name": "Main",
                "methods": [
                    {
                        "name": "main",
                        "description": "Entry point of the application, initializes managers and starts the web server."
                    }
                ]
            },
            {
                "name": "UserManager",
                "methods": [
                    {
                        "name": "register",
                        "description": "Registers a new user by saving their username, password, and email to users.txt."
                    },
                    {
                        "name": "login",
                        "description": "Validates user credentials against users.txt."
                    }
                ]
            },
            {
                "name": "ProductManager",
                "methods": [
                    {
                        "name": "load_products",
                        "description": "Loads product details from products.txt."
                    }
                ]
            },
            {
                "name": "CartManager",
                "methods": [
                    {
                        "name": "add_to_cart",
                        "description": "Adds a product to the user's shopping cart stored in cart.txt."
                    },
                    {
                        "name": "remove_from_cart",
                        "description": "Removes a product from the user's shopping cart stored in cart.txt."
                    },
                    {
                        "name": "view_cart",
                        "description": "Retrieves the contents of the user's shopping cart from cart.txt."
                    }
                ]
            },
            {
                "name": "OrderManager",
                "methods": [
                    {
                        "name": "create_order",
                        "description": "Creates a new order and saves it to orders.txt."
                    },
                    {
                        "name": "view_order_summary",
                        "description": "Retrieves the order summary based on the order ID from orders.txt."
                    }
                ]
            }
        ]
    }
},

"Task list": [
    "main.py",
    "templates/login.html",
    "templates/registration.html",
    "templates/product_listing.html",
    "templates/shopping_cart.html",
    "templates/checkout.html",
    "templates/order_confirmation.html",
    "users.txt",
    "products.txt",
    "cart.txt",
    "orders.txt"
],

"Shared Knowledge": {
    "coding standards": "Follow PEP 8 guidelines for Python code.",
    "file organization": "Keep all templates in the 'templates' directory, and ensure data files are in the root directory.",
    "testing strategies": "Implement unit tests for each manager class to ensure functionality works as expected."
}
[/CONTENT]