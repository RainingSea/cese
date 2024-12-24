# Software Description

## Objective
Develop a web application called 'Task_Manager' that allows users to create, manage, and track their tasks, using a local text file for data storage.

## Core Features

### Login Functionality:
1. Users can log in using their username and password.
2. The system validates the credentials against locally stored user data.
3. If validation fails, an error message ("Invalid username or password") is displayed.

### Registration Functionality:
1. Users can create a new account on the registration page by providing a username, password, and email.
2. The system checks for unique usernames and valid email formats.
3. Successful registration redirects users to the login page; failure provides appropriate error messages (e.g., "Username already exists").

### View Task List:
1. After login, users are redirected to the homepage displaying their task list.
2. Each task includes a description, due date, and status.

### Add New Tasks:
1. Users can add tasks by entering a task description and due date.
2. The new task is immediately displayed in the task list.

### Delete Tasks:
1. Each task has a "Delete" button to remove it from the list.

### Return to Login:
1. Users can click the "Back to Login" button to log out and return to the login page.

## Language
Use html and python to develop a web application.
You should use html to generate the web template by yourself.
## Data Storage
Data will be stored in local text files.
Different types of data will be stored in separate `.txt` files.
You should define the text file by yourself in advance.
This structured data storage will facilitate easy data retrieval and management through simple file manipulations in Python, ensuring the application remains light and efficient without the need for a SQL database.
