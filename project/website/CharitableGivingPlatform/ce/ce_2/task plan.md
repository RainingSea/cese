[CONTENT]
"Required packages": [
    "Flask",
    "os",
    "json"
],

"Required Other language third-party packages": [],

"Logic Analysis": {
    "main.py": {
        "description": "Main application file that initializes the Flask app and handles routing.",
        "classes": [
            {
                "name": "Main",
                "methods": [
                    {
                        "name": "main",
                        "description": "Starts the web application."
                    }
                ]
            }
        ]
    },
    "UserManager": {
        "description": "Handles user-related operations such as login and registration.",
        "methods": [
            {
                "name": "login",
                "description": "Validates user credentials."
            },
            {
                "name": "register",
                "description": "Registers a new user."
            },
            {
                "name": "load_users",
                "description": "Loads user data from 'users.txt'."
            }
        ]
    },
    "CharityManager": {
        "description": "Manages charity data and retrieval.",
        "methods": [
            {
                "name": "get_charities",
                "description": "Retrieves a list of available charities."
            },
            {
                "name": "get_charity_details",
                "description": "Retrieves detailed information about a specific charity."
            },
            {
                "name": "load_charities",
                "description": "Loads charity data from 'charities.txt'."
            }
        ]
    },
    "Contribution": {
        "description": "Handles contribution records for users.",
        "methods": [
            {
                "name": "add_contribution",
                "description": "Records a user's contribution to a charity."
            },
            {
                "name": "load_contributions",
                "description": "Loads contribution history from 'contributions.txt'."
            }
        ]
    }
},

"Task list": [
    "main.py",
    "user_manager.py",
    "charity_manager.py",
    "contribution.py",
    "templates/login.html",
    "templates/registration.html",
    "templates/dashboard.html",
    "templates/charity_details.html",
    "users.txt",
    "charities.txt",
    "contributions.txt"
],

"Shared Knowledge": [
    "Follow PEP 8 coding standards for Python code.",
    "Use meaningful variable and function names for clarity.",
    "Ensure proper error handling for file operations.",
    "Implement session management to maintain user login state."
]
[/CONTENT]