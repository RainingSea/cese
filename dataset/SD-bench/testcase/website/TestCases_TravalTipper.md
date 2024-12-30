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
  **Expectation**: An error message is displayed indicating that the login credentials are incorrect.

#### Functionality 3. Input Travel Details
- **Step**: Login successfully and navigate to the Travel Tips input section.  
  **Expectation**: The Travel Tips input form is displayed.  
- **Step**: Enter valid travel details (destination, trip duration, interests) and submit.  
  **Expectation**: Personalized travel tips are generated and displayed based on the input details.  
- **Step**: Submit the form with incomplete travel details.  
  **Expectation**: An error message is displayed indicating that all fields are required.

#### Functionality 4. View Recommendations
- **Step**: After inputting travel details, view the generated recommendations.  
  **Expectation**: Recommendations on local customs, safety tips, transportation options, cultural etiquette, and popular attractions are displayed.  
- **Step**: Refresh the page after viewing recommendations.  
  **Expectation**: The previously generated recommendations remain visible.

#### Functionality 5. Search for Tips
- **Step**: Navigate to the search section for travel tips.  
  **Expectation**: The search input field is displayed.  
- **Step**: Enter a specific destination or interest and submit the search.  
  **Expectation**: Relevant travel tips for the specified destination or interest are displayed.  
- **Step**: Enter a non-existent destination or interest.  
  **Expectation**: A message is displayed indicating that no tips were found.

#### Functionality 6. Save Favorite Travel Tips
- **Step**: View a list of travel tips.  
  **Step**: Click the "Save" button next to a travel tip.  
  **Expectation**: The travel tip is saved to the user's favorites, and a confirmation message is displayed.  
- **Step**: Navigate to the favorites section.  
  **Expectation**: The saved travel tips are displayed correctly.  
- **Step**: Attempt to save the same travel tip again.  
  **Expectation**: An error message is displayed indicating that the tip is already saved.

#### Functionality 7. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and an error message is displayed indicating that the user must log in.

#### Functionality 8. Navigate Back to Dashboard
- **Step**: Navigate to the Recommendations Page.  
- **Step**: Click the back button to return to the Dashboard Page.  
  **Expectation**: The user is redirected back to the Dashboard Page with the travel tips input form shown.  

#### Functionality 9. View Saved Travel Tips
- **Step**: Login successfully and navigate to the favorites section.  
  **Expectation**: The user's saved travel tips are displayed correctly.  
- **Step**: Click on a saved travel tip to view details.  
  **Expectation**: Detailed information about the selected travel tip is displayed.