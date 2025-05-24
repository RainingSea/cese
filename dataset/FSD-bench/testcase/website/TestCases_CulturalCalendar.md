### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration form is displayed.  
- **Step**: Enter a valid username and password, then submit the form.  
  **Expectation**: The user is registered successfully, and a confirmation message is displayed.  
- **Step**: Attempt to register with an already taken username.  
  **Expectation**: An error message is displayed indicating that the username is already in use.

#### Functionality 2. User Login
- **Step**: Navigate to the Login Page.  
  **Expectation**: The Login form is displayed.  
- **Step**: Enter a valid username and password.  
  **Expectation**: Access is granted, and the user is redirected to the Dashboard Page.  
- **Step**: Enter an invalid username or password.  
  **Expectation**: An error message is displayed indicating invalid credentials.

#### Functionality 3. View Upcoming Cultural Events on the Dashboard Page
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: A list of upcoming cultural events is displayed.  
- **Step**: Refresh the Dashboard Page after adding a new event in the local storage.  
  **Expectation**: The newly added event appears in the list of upcoming cultural events.

#### Functionality 4. View Event Details
- **Step**: Click on a specific event from the list on the Dashboard Page.  
  **Expectation**: The Event Details Page for that event is displayed, showing detailed information.  
- **Step**: Check the significance, history, and location information on the Event Details Page.  
  **Expectation**: All relevant details are displayed correctly.

#### Functionality 5. Search for Events
- **Step**: Navigate to the Dashboard Page and enter a keyword in the search bar.  
  **Expectation**: The list of events is filtered to show only those matching the keyword.  
- **Step**: Search by category and select a specific category from the dropdown.  
  **Expectation**: The list of events is filtered to show only those in the selected category.

#### Functionality 6. Set Reminder for an Event
- **Step**: Navigate to the Event Details Page for a specific event.  
- **Step**: Click the 'Set Reminder' button.  
  **Expectation**: The event is added to the user's reminders list, and a confirmation message is displayed.  
- **Step**: Navigate to the Reminders Page.  
  **Expectation**: The event appears in the list of reminders.

#### Functionality 7. View and Manage Reminders
- **Step**: Navigate to the Reminders Page after setting a reminder.  
  **Expectation**: The list of reminders is displayed, showing all events the user has set reminders for.  
- **Step**: Click on a reminder to remove it from the list.  
  **Expectation**: The reminder is removed successfully, and a confirmation message is displayed.

#### Functionality 8. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.

#### Functionality 9. Local Data Storage
- **Step**: Add a new cultural event to the local storage.  
- **Step**: Refresh the Dashboard Page.  
  **Expectation**: The newly added event appears in the list of upcoming cultural events.  
- **Step**: Remove an event from the local storage.  
- **Step**: Refresh the Dashboard Page.  
  **Expectation**: The removed event no longer appears in the list of upcoming cultural events.