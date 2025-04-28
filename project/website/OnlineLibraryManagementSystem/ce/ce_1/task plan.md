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
                        "description": "Entry point of the application that initializes managers and starts the application."
                    }
                ]
            },
            {
                "name": "UserManager",
                "methods": [
                    {
                        "name": "register",
                        "description": "Registers a new user by saving user details to 'users.txt'."
                    },
                    {
                        "name": "login",
                        "description": "Validates user credentials and creates a session."
                    },
                    {
                        "name": "logout",
                        "description": "Ends the user session and updates 'sessions.txt'."
                    },
                    {
                        "name": "view_users",
                        "description": "Returns a list of all registered users."
                    }
                ]
            },
            {
                "name": "BookManager",
                "methods": [
                    {
                        "name": "add_book",
                        "description": "Adds a new book entry to 'books.txt'."
                    },
                    {
                        "name": "delete_book",
                        "description": "Removes a book entry from 'books.txt'."
                    },
                    {
                        "name": "view_books",
                        "description": "Returns a list of all books in the library."
                    },
                    {
                        "name": "search_books",
                        "description": "Searches for books based on a query string."
                    }
                ]
            },
            {
                "name": "SessionManager",
                "methods": [
                    {
                        "name": "create_session",
                        "description": "Creates a new session for a logged-in user."
                    },
                    {
                        "name": "end_session",
                        "description": "Ends the session for a user."
                    }
                ]
            }
        ]
    }
},

"Task list": [
    "main.py",
    "templates/login.html",
    "templates/dashboard.html",
    "templates/book_management.html",
    "templates/user_management.html",
    "books.txt",
    "users.txt",
    "sessions.txt"
],

"Shared Knowledge": {
    "common practices": [
        "Use local text files for data storage to simplify data manipulation.",
        "Implement user authentication without encrypting passwords for simplicity.",
        "Organize the code into classes for better structure and maintainability.",
        "Ensure that the UI components are designed for seamless interaction."
    ]
}
[/CONTENT]