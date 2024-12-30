### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration form is displayed.  
- **Step**: Enter a valid username and password, then submit the form.  
  **Expectation**: The user is registered successfully, and a confirmation message is displayed.  
- **Step**: Attempt to register with an already existing username.  
  **Expectation**: An error message is displayed indicating that the username is already taken.

#### Functionality 2. User Login
- **Step**: Navigate to the Login Page.  
  **Expectation**: The Login form is displayed.  
- **Step**: Enter a valid username and password.  
  **Expectation**: Access is granted, and the user is redirected to the Dashboard Page.  
- **Step**: Enter an invalid username or password.  
  **Expectation**: An error message is displayed indicating that the credentials are incorrect.

#### Functionality 3. Create and Save Travel Journal Entries
- **Step**: Log in to the user account and navigate to the Journal Entry Page.  
  **Expectation**: The Journal Entry form is displayed.  
- **Step**: Fill in the form with valid details (destination, dates, activities, photos, reflections) and submit.  
  **Expectation**: The entry is saved successfully, and a confirmation message is displayed.  
- **Step**: Attempt to submit the form with missing required fields.  
  **Expectation**: An error message is displayed indicating which fields are required.

#### Functionality 4. View and Organize Past Entries
- **Step**: Log in to the user account and navigate to the Past Entries Page.  
  **Expectation**: A list of past entries is displayed.  
- **Step**: Filter entries by destination.  
  **Expectation**: Only entries matching the selected destination are displayed.  
- **Step**: Sort entries by date.  
  **Expectation**: The entries are displayed in chronological order.

#### Functionality 5. Edit or Delete Travel Entries
- **Step**: Navigate to the Past Entries Page and select an entry to edit.  
  **Expectation**: The entry details are displayed in an editable form.  
- **Step**: Modify the entry details and submit.  
  **Expectation**: The entry is updated successfully, and a confirmation message is displayed.  
- **Step**: Select an entry to delete.  
  **Expectation**: The entry is deleted successfully, and a confirmation message is displayed.

#### Functionality 6. Share Travel Entries
- **Step**: Navigate to a specific travel entry.  
  **Step**: Click the "Share" button.  
  **Expectation**: A shareable link is generated and displayed.  
- **Step**: Attempt to share an entry that has not been saved.  
  **Expectation**: An error message is displayed indicating that the entry must be saved before sharing.

#### Functionality 7. Search for Specific Entries or Destinations
- **Step**: Navigate to the Search Page.  
  **Expectation**: The search input field is displayed.  
- **Step**: Enter a keyword related to an entry or destination and submit.  
  **Expectation**: The search results display entries that match the keyword.  
- **Step**: Enter a keyword that does not match any entries.  
  **Expectation**: A message is displayed indicating that no entries were found.

#### Functionality 8. User Logout
- **Step**: Click the "Logout" button on the Dashboard Page.  
  **Expectation**: The user is logged out and redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected to the Login Page with a message indicating that they need to log in.

#### Functionality 9. Navigate Back to Dashboard
- **Step**: While viewing a specific travel entry, click the "Back to Dashboard" button.  
  **Expectation**: The user is redirected back to the Dashboard Page.  
- **Step**: Refresh the Dashboard Page after making changes to an entry.  
  **Expectation**: The updated entries are displayed correctly on the Dashboard Page.