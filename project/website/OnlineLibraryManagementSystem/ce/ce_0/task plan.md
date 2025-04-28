[CONTENT]
"Required packages": ["os", "json"],

"Required Other language third-party packages": [],

"Logic Analysis": [
    {
        "filename": "main.py",
        "classes": [
            {
                "name": "Main",
                "methods": [
                    {
                        "name": "main",
                        "description": "Entry point of the application, initializes user and book managers."
                    }
                ]
            },
            {
                "name": "UserManager",
                "methods": [
                    {
                        "name": "register",
                        "description": "Registers a new user by saving username and password to users.txt."
                    },
                    {
                        "name": "login",
                        "description": "Validates user credentials and starts a user session."
                    },
                    {
                        "name": "logout",
                        "description": "Ends the user session and updates sessions.txt."
                    },
                    {
                        "name": "view_users",
                        "description": "Retrieves and returns a list of all registered users."
                    }
                ]
            },
            {
                "name": "BookManager",
                "methods": [
                    {
                        "name": "add_book",
                        "description": "Adds a new book entry to books.txt."
                    },
                    {
                        "name": "delete_book",
                        "description": "Removes a book entry from books.txt using its ISBN."
                    },
                    {
                        "name": "view_books",
                        "description": "Retrieves and returns a list of all books."
                    },
                    {
                        "name": "search_books",
                        "description": "Searches for books based on a query and returns matching results."
                    }
                ]
            }
        ]
    },
    {
        "filename": "templates/login.html",
        "description": "HTML template for user login form."
    },
    {
        "filename": "templates/dashboard.html",
        "description": "HTML template for the main dashboard interface."
    },
    {
        "filename": "templates/book_management.html",
        "description": "HTML template for managing books (add, delete, view)."
    },
    {
        "filename": "templates/user_management.html",
        "description": "HTML template for managing user accounts (add, view)."
    },
    {
        "filename": "templates/search.html",
        "description": "HTML template for searching books."
    },
    {
        "filename": "users.txt",
        "description": "Text file for storing user account information."
    },
    {
        "filename": "books.txt",
        "description": "Text file for storing book details."
    },
    {
        "filename": "sessions.txt",
        "description": "Text file for managing user sessions."
    }
],

"Task list": [
    "main.py",
    "templates/login.html",
    "templates/dashboard.html",
    "templates/book_management.html",
    "templates/user_management.html",
    "templates/search.html",
    "users.txt",
    "books.txt",
    "sessions.txt"
],

"Shared Knowledge": "The project will utilize local text files for data storage, which simplifies the implementation by avoiding SQL databases. The user interface will be built using HTML, and the backend logic will be implemented in Python. Each functionality is modularized into classes for user and book management, ensuring maintainability and scalability."
[/CONTENT]