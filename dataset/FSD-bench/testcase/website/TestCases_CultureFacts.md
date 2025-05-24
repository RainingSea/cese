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

#### Functionality 3. Explore Cultures on the Dashboard Page 
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: A list of available cultures is displayed.  
- **Step**: Click on a culture from the list.  
  **Expectation**: The user is redirected to the Culture Details Page for the selected culture.

#### Functionality 4. View Culture Details 
- **Step**: Navigate to the Dashboard Page and select a culture.  
  **Expectation**: The Culture Details Page is displayed with detailed information about the culture.  
- **Step**: Check if the history, traditions, and unique aspects of the culture are present.  
  **Expectation**: All relevant details are displayed correctly on the Culture Details Page.

#### Functionality 5. Search for Cultures or Facts 
- **Step**: Navigate to the Dashboard Page.  
  **Step**: Enter a keyword in the search bar and submit.  
  **Expectation**: The search results display cultures or facts that match the keyword.  
- **Step**: Search for a keyword that does not exist.  
  **Expectation**: A message is displayed indicating that no results were found.

#### Functionality 6. Bookmark Culture Facts 
- **Step**: Navigate to the Culture Details Page for a specific culture.  
  **Step**: Click the "Bookmark" button.  
  **Expectation**: The culture fact is added to the user's bookmarks, and a confirmation message is displayed.  
- **Step**: Navigate to the Bookmarks Page.  
  **Expectation**: The bookmarked culture facts are displayed correctly.

#### Functionality 7. View and Manage Bookmarks 
- **Step**: Navigate to the Bookmarks Page after bookmarking several culture facts.  
  **Expectation**: All bookmarked culture facts are displayed.  
- **Step**: Click on the "Remove" button next to a bookmarked fact.  
  **Expectation**: The fact is removed from the bookmarks, and a confirmation message is displayed.

#### Functionality 8. User Logout 
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.

#### Functionality 9. Local Data Storage 
- **Step**: Add a new culture fact to the local storage.  
- **Step**: Refresh the Dashboard Page.  
  **Expectation**: The newly added culture fact appears in the culture list.  
- **Step**: Check the local text file for the culture facts.  
  **Expectation**: The new culture fact is present in the appropriate text file.