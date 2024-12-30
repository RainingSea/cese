### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration form is displayed with fields for username and password.  
- **Step**: Enter a valid username and password, then submit the form.  
  **Expectation**: The user is registered successfully, and a confirmation message is displayed.  
- **Step**: Attempt to register with an already existing username.  
  **Expectation**: An error message is displayed indicating that the username is already taken.

#### Functionality 2. User Login
- **Step**: Navigate to the Login Page.  
  **Expectation**: The Login form is displayed with fields for username and password.  
- **Step**: Enter a valid username and password.  
  **Expectation**: Access is granted, and the user is redirected to the Dashboard Page.  
- **Step**: Enter an invalid username or password.  
  **Expectation**: An error message is displayed indicating that the login credentials are incorrect.

#### Functionality 3. Equipment Management on Dashboard Page
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: The equipment management interface is displayed.  
- **Step**: Input details for a new equipment item (e.g., name, type, condition, location) and submit.  
  **Expectation**: The new equipment item is added to the inventory and displayed in the list.  
- **Step**: Update the details of an existing equipment item.  
  **Expectation**: The updated information is reflected in the equipment list.

#### Functionality 4. View Equipment Details
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: A list of available equipment is displayed.  
- **Step**: Click on a specific equipment item to view its details.  
  **Expectation**: Detailed information about the selected equipment item is displayed, including quantity, condition, availability, and location.

#### Functionality 5. Set Alerts for Equipment Maintenance
- **Step**: Navigate to the Dashboard Page and select an equipment item.  
  **Step**: Set a maintenance alert for the equipment.  
  **Expectation**: The alert is saved, and a confirmation message is displayed.  
- **Step**: Check the alerts section for the equipment item.  
  **Expectation**: The maintenance alert is listed with the correct details.

#### Functionality 6. Search for Equipment
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Step**: Enter a specific equipment name in the search bar.  
  **Expectation**: The equipment list is filtered to show only the matching items.  
- **Step**: Search for equipment by type or location.  
  **Expectation**: The equipment list is filtered accordingly, displaying relevant results.

#### Functionality 7. Filter Equipment List
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Step**: Apply a filter based on equipment condition (e.g., "Good").  
  **Expectation**: The equipment list updates to show only items that match the selected condition.  
- **Step**: Clear the filter.  
  **Expectation**: The full equipment list is displayed again.

#### Functionality 8. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.

#### Functionality 9. Data Persistence
- **Step**: Login successfully and add a new equipment item.  
  **Step**: Logout and close the application.  
  **Step**: Reopen the application and log in again.  
  **Expectation**: The previously added equipment item is still present in the inventory list.