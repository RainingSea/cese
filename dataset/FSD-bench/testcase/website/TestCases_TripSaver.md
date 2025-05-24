### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password, then submit the form.  
  **Expectation**: The user is registered successfully, and a confirmation message is displayed.  
- **Step**: Attempt to register with an already existing username.  
  **Expectation**: An error message is displayed indicating that the username is already taken.  

#### Functionality 2. User Login
- **Step**: Navigate to the Login Page.  
  **Expectation**: The Login Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password.  
  **Expectation**: Access is granted, and the user is redirected to the Dashboard Page.  
- **Step**: Enter an invalid username or password.  
  **Expectation**: An error message is displayed indicating that the credentials are incorrect.  

#### Functionality 3. Input Trip Details
- **Step**: Login successfully and navigate to the Trip Details input page.  
  **Expectation**: The Trip Details input form is displayed with fields for starting point, destination, and travel date.  
- **Step**: Fill in the trip details with valid information and submit.  
  **Expectation**: The trip details are saved successfully, and the user is redirected to the suggestions page.  
- **Step**: Leave one or more fields empty and attempt to submit.  
  **Expectation**: An error message is displayed indicating that all fields are required.  

#### Functionality 4. View Transportation Suggestions
- **Step**: After inputting trip details, view the transportation suggestions.  
  **Expectation**: A list of transportation options is displayed with estimated costs and travel times.  
- **Step**: Compare different transportation options based on distance, cost, and time.  
  **Expectation**: The comparison is displayed clearly, allowing the user to make an informed decision.  

#### Functionality 5. Save Preferred Transportation Options
- **Step**: View the transportation suggestions after inputting trip details.  
  **Step**: Select a preferred transportation option and click the save button.  
  **Expectation**: The preferred option is saved successfully, and a confirmation message is displayed.  
- **Step**: Navigate to the saved options page.  
  **Expectation**: The previously saved transportation options are displayed correctly.  

#### Functionality 6. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.  

#### Functionality 7. View Estimated Costs and Travel Times
- **Step**: After inputting trip details, view the transportation suggestions.  
  **Expectation**: The estimated costs and travel times for each transportation option are displayed.  
- **Step**: Select a transportation option and view its detailed information.  
  **Expectation**: Detailed information about costs and travel times for the selected option is displayed.  

#### Functionality 8. Compare Transportation Options
- **Step**: After viewing transportation suggestions, select multiple options for comparison.  
  **Expectation**: A comparison view is displayed showing distance, cost, and time for each selected option.  
- **Step**: Change the trip details and view the updated comparison.  
  **Expectation**: The comparison updates correctly based on the new trip details.  