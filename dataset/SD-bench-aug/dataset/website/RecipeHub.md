# Software Description

## Objective
The task is to develop a comprehensive web application, 'OnlineVintageMarket', for buying and selling vintage items that utilizes Python and stores information in local text files, eliminating the need for SQL databases. Note that the website should start from the login page.

## core features
### Login Functionality
1. Users can log in by entering a username and password on the Login Page.
2. If the login is successful, users will be redirected to the Home Page and see a personalized welcome message.
3. If the login fails (e.g., incorrect username or password), the Login Page will display an appropriate error message.
4. Users can navigate to the Registration Page by clicking the Register button on the Login Page.
### Registration Functionality
1. Users can register by entering a username and password on the Registration Page.
2. Upon successful registration, users will be redirected to the Login Page and see a message: "Registration successful, please log in."
3. If the username already exists or the input is invalid (e.g., the password is too short), the Registration Page will display an appropriate error message.
### Home Page Functionality
1. After a successful login, users will see a personalized welcome message, such as "Welcome back, [Username]!".
2. Users can navigate to the following pages from the Home Page:
   Recipe Submission Page: Via the "Submit a New Recipe" button.
   Recipe Browsing Page: Via the "Browse Recipes" button.
3. Users can log out via the top navigation bar or the "Log Out" button, which will return them to the Login Page.
### Recipe Submission Functionality
1. Users can submit a recipe by filling out the title, ingredients, and instructions on the Recipe Submission Page.
2. Upon successful submission, the system will display a success message and provide a button to return to the Home Page.
3. If the submission fails (e.g., required fields are empty), the system will prompt users to complete the missing information and resubmit.
### Recipe Browsing Functionality
1. Users can search for recipes by entering keywords on the Recipe Browsing Page, and the system will display a list of matching recipes.
2. Users can click on any recipe title from the list to navigate to the Recipe Details Page for more information.
3. Users can return to the Home Page from the Recipe Browsing Page using the "Back to Home" button.
### Recipe Details Functionality
1. Users can view complete information about a selected recipe, including the title, ingredients, and instructions, on the Recipe Details Page.
2. Users can return to the Home Page from the Recipe Details Page using the "Back to Home" button.

## Language
Use html and python to develop a web application.
You should use html to generate the web template by yourself.

## Data Storage
Data will be stored in local text files.
Different types of data will be stored in separate `.txt` files.
You should define the text file by yourself in advance.
This structured data storage will facilitate easy data retrieval and management through simple file manipulations in Python, ensuring the application remains light and efficient without the need for a SQL database.