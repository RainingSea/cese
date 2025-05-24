### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password and submit the registration form.  
  **Expectation**: The user is registered successfully, and a confirmation message is displayed.  
- **Step**: Attempt to register with an already existing username.  
  **Expectation**: An error message is displayed indicating that the username is already taken.

#### Functionality 2. User Login
- **Step**: Navigate to the Login Page.  
  **Expectation**: The Login Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password.  
  **Expectation**: Access is granted, and the user is redirected to the Dashboard Page.  
- **Step**: Enter an invalid username or password.  
  **Expectation**: An error message is displayed indicating that the login credentials are incorrect.

#### Functionality 3. Feedback Submission
- **Step**: Log in successfully and navigate to the feedback submission page.  
  **Expectation**: The feedback submission form is displayed.  
- **Step**: Fill in the feedback form with valid details and submit it.  
  **Expectation**: The feedback is submitted successfully, and a confirmation message is displayed.  
- **Step**: Attempt to submit feedback without filling in required fields.  
  **Expectation**: An error message is displayed indicating that all required fields must be filled.

#### Functionality 4. Feedback Categorization
- **Step**: Log in successfully and navigate to the feedback submission page.  
  **Step**: Select a category from the predefined categories dropdown.  
  **Expectation**: The selected category is displayed correctly in the feedback form.  
- **Step**: Submit feedback with a selected category.  
  **Expectation**: The feedback is categorized correctly and stored in the appropriate text file.

#### Functionality 5. Manager Review of Feedback
- **Step**: Log in as a manager and navigate to the feedback review page.  
  **Expectation**: A list of submitted feedback is displayed with their statuses.  
- **Step**: Click on a specific feedback entry to view details.  
  **Expectation**: The details of the selected feedback are displayed, including the category and status.

#### Functionality 6. View Feedback Status
- **Step**: Log in successfully and navigate to the feedback status page.  
  **Expectation**: A list of the user's submitted feedback along with their statuses is displayed.  
- **Step**: Refresh the feedback status page after a manager updates the status of a feedback entry.  
  **Expectation**: The updated status is reflected correctly on the user's feedback status page.

#### Functionality 7. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to navigate to the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.

#### Functionality 8. Return to Login Page
- **Step**: On the Dashboard Page, click the "Logout" button.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: On the Login Page, click the "Register here" link.  
  **Expectation**: The user is redirected to the Registration Page.