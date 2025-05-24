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
  **Expectation**: An error message is displayed indicating invalid credentials.

#### Functionality 3. Input Travel Preferences
- **Step**: Login successfully and navigate to the preferences input page.  
  **Expectation**: The preferences input form is displayed with fields for budget, activities, and climate.  
- **Step**: Fill in the travel preferences and submit the form.  
  **Expectation**: The preferences are saved successfully, and the user is redirected to the recommendations page.

#### Functionality 4. Generate Travel Recommendations
- **Step**: After inputting travel preferences, click on the "Get Recommendations" button.  
  **Expectation**: A list of personalized travel destinations is displayed based on the user's preferences.  
- **Step**: Check the details of a recommended destination.  
  **Expectation**: Detailed information about the destination, including popular activities, climate, and travel costs, is displayed.

#### Functionality 5. Save Favorite Destinations
- **Step**: View the list of recommended destinations.  
  **Step**: Click the "Save" button next to a destination.  
  **Expectation**: The destination is added to the user's favorites list, and a confirmation message is displayed.  
- **Step**: Navigate to the favorites list.  
  **Expectation**: The saved destination appears in the favorites list.

#### Functionality 6. User Logout
- **Step**: Click the "Logout" button on the Dashboard Page.  
  **Expectation**: The user is logged out and redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.

#### Functionality 7. View Detailed Information About Destinations
- **Step**: Click on a recommended destination from the list.  
  **Expectation**: The detailed information page for that destination is displayed.  
- **Step**: Check the details for multiple destinations.  
  **Expectation**: Each destination's detailed information is displayed correctly without errors.