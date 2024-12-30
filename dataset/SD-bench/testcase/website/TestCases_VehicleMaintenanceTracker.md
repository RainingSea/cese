### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password, then submit the form.  
  **Expectation**: The user is registered successfully, and a confirmation message is displayed.  
- **Step**: Attempt to register with an existing username.  
  **Expectation**: An error message is displayed indicating that the username is already taken.  

#### Functionality 2. User Login
- **Step**: Navigate to the Login Page.  
  **Expectation**: The Login Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password.  
  **Expectation**: Access is granted, and the user is redirected to the Dashboard Page.  
- **Step**: Enter an invalid username or password.  
  **Expectation**: An error message is displayed indicating that the login credentials are incorrect.  

#### Functionality 3. Input Vehicle Information
- **Step**: Log in successfully and navigate to the Vehicle Information Page.  
  **Expectation**: The Vehicle Information Page is displayed with fields for make, model, year, and mileage.  
- **Step**: Enter valid vehicle information and submit the form.  
  **Expectation**: The vehicle information is saved successfully, and a confirmation message is displayed.  
- **Step**: Attempt to enter invalid vehicle information (e.g., negative mileage).  
  **Expectation**: An error message is displayed indicating that the input is invalid.  

#### Functionality 4. Track Regular Maintenance Tasks
- **Step**: Log in successfully and navigate to the Maintenance Tracker Page.  
  **Expectation**: The Maintenance Tracker Page is displayed with options to add maintenance tasks.  
- **Step**: Enter a valid maintenance task (e.g., oil change) and submit.  
  **Expectation**: The maintenance task is saved successfully, and a confirmation message is displayed.  
- **Step**: Attempt to add a maintenance task without specifying a task type.  
  **Expectation**: An error message is displayed indicating that the task type is required.  

#### Functionality 5. Send Reminders and Notifications
- **Step**: Log in successfully and navigate to the Maintenance Tracker Page.  
  **Step**: Add a maintenance task with a predefined interval (e.g., every 5000 miles).  
  **Expectation**: The task is saved, and a reminder notification is scheduled.  
- **Step**: Simulate reaching the mileage threshold for the maintenance task.  
  **Expectation**: The user receives a notification reminding them of the upcoming maintenance task.  

#### Functionality 6. View Maintenance History
- **Step**: Log in successfully and navigate to the Maintenance History Page.  
  **Expectation**: The Maintenance History Page is displayed with a list of past maintenance records.  
- **Step**: Check the maintenance history after adding a new maintenance record.  
  **Expectation**: The newly added maintenance record appears in the history list.  

#### Functionality 7. Update or Delete Maintenance Records
- **Step**: Log in successfully and navigate to the Maintenance History Page.  
  **Step**: Select a maintenance record to update.  
  **Expectation**: The update form is displayed with the current record information.  
- **Step**: Modify the record and submit the update.  
  **Expectation**: The maintenance record is updated successfully, and a confirmation message is displayed.  
- **Step**: Select a maintenance record to delete.  
  **Step**: Confirm the deletion.  
  **Expectation**: The maintenance record is deleted successfully, and a confirmation message is displayed.  

#### Functionality 8. User Logout
- **Step**: Log in successfully and navigate to the Dashboard Page.  
  **Step**: Click the logout button.  
  **Expectation**: The user is logged out and redirected to the Login Page.  

#### Functionality 9. Navigate Back to Dashboard
- **Step**: Log in successfully and navigate to the Maintenance Tracker Page.  
- **Step**: Click the back button to return to the Dashboard Page.  
  **Expectation**: The user is redirected back to the Dashboard Page with the vehicle and maintenance information displayed.  

#### Functionality 10. View and Update Vehicle Information
- **Step**: Log in successfully and navigate to the Vehicle Information Page.  
- **Step**: View the existing vehicle information.  
  **Expectation**: The current vehicle information is displayed correctly.  
- **Step**: Update the vehicle information and submit.  
  **Expectation**: The vehicle information is updated successfully, and a confirmation message is displayed.  