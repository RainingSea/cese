[CONTENT]
"Required packages": ["Flask"],

"Required Other language third-party packages": [],

"Logic Analysis": [
    {
        "file": "main.py",
        "classes": [
            {
                "name": "UserManager",
                "methods": [
                    {"name": "register", "description": "Register a new user with username and password."},
                    {"name": "login", "description": "Verify user credentials for login."},
                    {"name": "user_exists", "description": "Check if a username already exists."},
                    {"name": "_load_users", "description": "Load users data from users.txt."},
                    {"name": "_save_user", "description": "Save a new user to users.txt."}
                ]
            },
            {
                "name": "BookManager",
                "methods": [
                    {"name": "search_books", "description": "Search books by title, author, or keywords."},
                    {"name": "get_book", "description": "Retrieve detailed info for a specific book."},
                    {"name": "_load_books", "description": "Load books data from books.txt."}
                ]
            },
            {
                "name": "ReadingListManager",
                "methods": [
                    {"name": "add_book", "description": "Add a book to user's reading list."},
                    {"name": "get_reading_list", "description": "Retrieve user's reading list."},
                    {"name": "remove_book", "description": "Remove a book from user's reading list."},
                    {"name": "_load_reading_list", "description": "Load reading list data from reading_lists.txt."},
                    {"name": "_save_reading_list_entry", "description": "Save a new reading list entry."},
                    {"name": "_save_all_reading_list", "description": "Save all reading list entries."}
                ]
            }
        ],
        "functions": [
            {"name": "setup_routes", "description": "Define Flask routes for registration, login, dashboard, book details, reading list, and logout."},
            {"name": "run", "description": "Start the Flask web server."}
        ]
    }
],

"Task list": [
    "main.py",
    "templates/login.html",
    "templates/register.html",
    "templates/dashboard.html",
    "templates/book_details.html",
    "templates/reading_list.html"
],

"Shared Knowledge": "Ensure that all file operations for users, books, and reading lists are handled carefully to prevent data corruption. Passwords are stored as plain text, so handle input securely but avoid encryption or hashing. The web app should be simple, with forms submitting data via POST requests, and results displayed on the same or new pages. Routes should handle session management minimally, possibly via Flask session or cookies, to maintain user login state. The application design emphasizes file-based data management without database dependencies, so loading and saving data should be optimized for small datasets. HTML templates should be straightforward, with forms and links to navigate between pages, and include logout links for user convenience."
[/CONTENT]