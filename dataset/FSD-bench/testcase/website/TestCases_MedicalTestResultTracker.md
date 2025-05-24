### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password, then submit the registration form.  
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

#### Functionality 3. Input and Manage Medical Test Results
- **Step**: Log in successfully and navigate to the Test Results Page.  
  **Expectation**: The Test Results Page is displayed with options to add new test results.  
- **Step**: Input valid medical test results and submit.  
  **Expectation**: The test results are saved successfully, and a confirmation message is displayed.  
- **Step**: Attempt to input invalid test results (e.g., negative values for a test that cannot be negative).  
  **Expectation**: An error message is displayed indicating that the input is invalid.

#### Functionality 4. View Historical Data and Trends
- **Step**: Log in successfully and navigate to the Trends Page.  
  **Expectation**: The Trends Page is displayed with historical data visualizations.  
- **Step**: Select a specific test type to view its trends over time.  
  **Expectation**: The trends for the selected test type are displayed correctly, showing changes over time.

#### Functionality 5. Set and Receive Reminders
- **Step**: Log in successfully and navigate to the Reminders Page.  
  **Expectation**: The Reminders Page is displayed with options to set new reminders.  
- **Step**: Set a reminder for a follow-up test and save it.  
  **Expectation**: The reminder is saved successfully, and a confirmation message is displayed.  
- **Step**: Check the reminders list after setting a reminder.  
  **Expectation**: The newly set reminder appears in the reminders list.

#### Functionality 6. View Test Result History
- **Step**: Log in successfully and navigate to the Test Result History Page.  
  **Expectation**: The Test Result History Page is displayed with a list of past test results.  
- **Step**: Click on a specific test result to view its details.  
  **Expectation**: The details of the selected test result are displayed correctly.

#### Functionality 7. User Logout
- **Step**: Log in successfully and navigate to the Dashboard Page.  
  **Step**: Click the logout button.  
  **Expectation**: The user is logged out and redirected to the Login Page.  

#### Functionality 8. Navigate Back to Dashboard
- **Step**: Navigate to the Test Results Page after logging in.  
- **Step**: Click the back button to return to the Dashboard Page.  
  **Expectation**: The user is redirected back to the Dashboard Page with the relevant information displayed.  

#### Functionality 9. View Test Result Details
- **Step**: Log in successfully and navigate to the Test Results Page.  
- **Step**: Click on a specific test result to view its details.  
  **Expectation**: The details of the selected test result are displayed correctly, showing all relevant information.