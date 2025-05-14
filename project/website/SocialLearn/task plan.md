[CONTENT]
"Required packages": "flask",

"Required Other language third-party packages": "",

"Logic Analysis": {
    "main.py": {
        "description": "Main application file with Flask setup and route definitions",
        "components": [
            "Flask app initialization",
            "Route for home page",
            "Route protection decorator (login_required)",
            "Session management setup"
        ]
    },
    "managers.py": {
        "description": "Contains all manager classes for handling business logic",
        "classes": {
            "UserManager": [
                "register(username, password): Handle new user registration",
                "login(username, password): Authenticate users",
                "user_exists(username): Check for duplicate usernames"
            ],
            "ProfileManager": [
                "get_profile(username): Retrieve user profile data",
                "update_profile(username, interests, expertise): Update profile info"
            ],
            "GroupManager": [
                "list_groups(): Return all available groups",
                "join_group(username, groupname): Add user to group"
            ],
            "ResourceManager": [
                "add_resource(title, content, author, group): Store new resource",
                "get_resources(group): Retrieve group-specific resources"
            ],
            "MessageManager": [
                "send_message(sender, receiver, content): Store new message",
                "get_messages(user): Retrieve user's messages"
            ]
        }
    },
    "templates/base.html": {
        "description": "Base template with navigation bar and common layout",
        "components": [
            "Navigation bar with conditional links (login/register vs profile/logout)",
            "Block for content injection",
            "Error message display area"
        ]
    },
    "templates/login.html": {
        "description": "User login form",
        "components": [
            "Username/password input fields",
            "Form validation",
            "Link to registration page"
        ]
    },
    "templates/register.html": {
        "description": "User registration form",
        "components": [
            "Username/password input fields",
            "Duplicate username check",
            "Link to login page"
        ]
    },
    "templates/profile.html": {
        "description": "Profile management interface",
        "components": [
            "Profile display section",
            "Editable fields for interests/expertise",
            "Update button"
        ]
    },
    "templates/groups.html": {
        "description": "Study group interface",
        "components": [
            "List of available groups",
            "Join group buttons",
            "Group-specific resource section"
        ]
    },
    "templates/resources.html": {
        "description": "Resource sharing interface",
        "components": [
            "Resource submission form",
            "List of existing resources",
            "Resource filtering by group"
        ]
    },
    "templates/messages.html": {
        "description": "Messaging interface",
        "components": [
            "Message list",
            "New message form",
            "Message threading"
        ]
    }
},

"Task list": [
    "main.py",
    "managers.py",
    "templates/base.html",
    "templates/login.html",
    "templates/register.html",
    "templates/profile.html",
    "templates/groups.html",
    "templates/resources.html",
    "templates/messages.html",
    "users.txt",
    "profiles.txt",
    "groups.txt",
    "resources.txt",
    "messages.txt"
],

"Shared Knowledge": [
    "All data stored in pipe-delimited text files",
    "No password encryption for demo purposes",
    "Session-based authentication without persistent login",
    "Error handling required for file operations",
    "Input validation needed for all forms",
    "Route protection required for authenticated pages",
    "Template inheritance from base.html",
    "Current user state must be passed to all templates"
]
[/CONTENT]