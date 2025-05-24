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
  **Expectation**: An error message is displayed indicating that the credentials are incorrect.

#### Functionality 3. Manage Medical Information
- **Step**: Log in successfully and navigate to the Medical Information section.  
  **Expectation**: The user can view their current medical information.  
- **Step**: Input new medical information (diagnosis, medication, treatment) and save.  
  **Expectation**: The new information is saved successfully and displayed in the medical information list.  
- **Step**: Edit existing medical information and save changes.  
  **Expectation**: The changes are saved successfully and reflected in the medical information list.

#### Functionality 4. Set and Receive Appointment Reminders
- **Step**: Log in successfully and navigate to the Appointment Reminders section.  
  **Expectation**: The user can view existing appointment reminders.  
- **Step**: Set a new appointment reminder with a valid date and time.  
  **Expectation**: The reminder is saved successfully and displayed in the appointment reminders list.  
- **Step**: Attempt to set an appointment reminder with an invalid date format.  
  **Expectation**: An error message is displayed indicating that the date format is invalid.

#### Functionality 5. View and Edit Medical History
- **Step**: Log in successfully and navigate to the Medical History section.  
  **Expectation**: The user can view their complete medical history.  
- **Step**: Click on an entry to edit it.  
  **Expectation**: The user is able to edit the selected entry and save changes.  
- **Step**: Attempt to delete a medical history entry.  
  **Expectation**: The entry is removed from the medical history list successfully.

#### Functionality 6. User Logout
- **Step**: Log in successfully and navigate to the Dashboard Page.  
  **Expectation**: The Dashboard Page is displayed.  
- **Step**: Click the logout button.  
  **Expectation**: The user is logged out and redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected to the Login Page, and access to the Dashboard is denied.