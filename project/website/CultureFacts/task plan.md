[CONTENT]
"Logic Analysis": 
- **Main**: This class will handle the main application logic and routing for the web application. It will initialize the user, culture, and bookmark managers.
- **UserManager**: Responsible for managing user accounts, including registration and login functionalities. It will handle error messages for failed login attempts and registrations.
- **CultureManager**: Manages culture-related data, including retrieving all cultures, getting details for a specific culture, and searching cultures based on keywords.
- **BookmarkManager**: Handles bookmarking functionalities, allowing users to add, remove, and view their bookmarks. It will ensure bookmarks are associated with specific users.

"Task list": 
[
    "main.py - Contains the main application logic and routing.",
    "templates/registration.html - HTML template for user registration.",
    "templates/login.html - HTML template for user login.",
    "templates/dashboard.html - HTML template for the culture dashboard.",
    "templates/culture_details.html - HTML template for displaying culture details.",
    "templates/bookmarks.html - HTML template for managing bookmarks.",
    "users.txt - Text file for storing user account information.",
    "cultures.txt - Text file for storing culture facts and details.",
    "bookmarks.txt - Text file for storing user bookmarks."
],

"Shared Knowledge": Include relevant information about the Flask framework, focusing on its routing capabilities and how to handle form submissions without using flask_wtf. Emphasize the importance of user experience in the UI design, ensuring that feedback messages for registration and login processes are clear and informative. Highlight the significance of managing user sessions effectively to enhance the overall functionality of the application.
[/CONTENT]