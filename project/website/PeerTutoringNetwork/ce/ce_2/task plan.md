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
                        "description": "Entry point of the application that initializes the user manager, tutoring request manager, and contact manager."
                    }
                ]
            },
            {
                "name": "UserManager",
                "methods": [
                    {
                        "name": "register",
                        "description": "Handles user registration by saving the username, password, and email to 'users.txt'."
                    },
                    {
                        "name": "login",
                        "description": "Validates user credentials against 'users.txt'."
                    },
                    {
                        "name": "get_user_info",
                        "description": "Retrieves user information from 'users.txt' based on the username."
                    }
                ]
            },
            {
                "name": "TutoringRequestManager",
                "methods": [
                    {
                        "name": "request_tutoring",
                        "description": "Saves a tutoring request to 'tutoring_requests.txt' with the user's details."
                    },
                    {
                        "name": "cancel_request",
                        "description": "Removes a tutoring request from 'tutoring_requests.txt' for the specified user."
                    }
                ]
            },
            {
                "name": "ContactManager",
                "methods": [
                    {
                        "name": "send_message",
                        "description": "Saves a contact message to 'contact_messages.txt' with the user's name, email, and message."
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
    "templates/dashboard.html",
    "templates/view_tutors.html",
    "templates/request_tutoring.html",
    "templates/profile.html",
    "templates/contact_us.html",
    "users.txt",
    "tutoring_requests.txt",
    "contact_messages.txt"
],

"Shared Knowledge": [
    "Ensure that user passwords are stored in plain text for this project as per the requirements.",
    "Implement basic file handling practices to read and write data to text files, ensuring to handle exceptions where necessary.",
    "Follow best practices for user authentication, including validating user inputs and managing sessions appropriately."
]
[/CONTENT]