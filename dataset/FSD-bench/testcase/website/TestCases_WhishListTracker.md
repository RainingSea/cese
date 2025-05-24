### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration form is displayed.  
- **Step**: Enter a valid username and password, then submit the form.  
  **Expectation**: The user is registered successfully, and a confirmation message is displayed.  
- **Step**: Attempt to register with an existing username.  
  **Expectation**: An error message is displayed indicating that the username is already taken.  

#### Functionality 2. User Login
- **Step**: Navigate to the Login Page.  
  **Expectation**: The Login form is displayed.  
- **Step**: Enter a valid username and password.  
  **Expectation**: Access is granted, and the user is redirected to the Dashboard Page.  
- **Step**: Enter an invalid username or password.  
  **Expectation**: An error message is displayed indicating that the credentials are incorrect.  

#### Functionality 3. Add Items to Wishlist
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: The Dashboard is displayed with an option to add items.  
- **Step**: Enter item name, description, and desired price, then submit the form.  
  **Expectation**: The item is added to the wishlist, and a success message is displayed.  
- **Step**: Attempt to add an item with missing required fields (e.g., item name).  
  **Expectation**: An error message is displayed indicating that all fields are required.  

#### Functionality 4. View Wishlist
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: The wishlist is displayed, showing all added items with their details.  
- **Step**: Refresh the Dashboard Page after adding a new item.  
  **Expectation**: The newly added item appears in the wishlist.  

#### Functionality 5. Update Item in Wishlist
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Step**: Select an item from the wishlist to update.  
  **Expectation**: The item details are displayed for editing.  
- **Step**: Modify the item details and submit the changes.  
  **Expectation**: The item is updated successfully, and a confirmation message is displayed.  

#### Functionality 6. Remove Item from Wishlist
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Step**: Select an item from the wishlist to remove.  
  **Expectation**: The item is removed from the wishlist, and a success message is displayed.  
- **Step**: Attempt to remove an item that does not exist in the wishlist.  
  **Expectation**: An error message is displayed indicating that the item cannot be found.  

#### Functionality 7. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to navigate back to the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access to the Dashboard is denied.  

#### Functionality 8. Data Persistence
- **Step**: Login successfully and add an item to the wishlist.  
  **Step**: Logout and close the application.  
  **Step**: Reopen the application and log back in.  
  **Expectation**: The previously added item is still present in the wishlist, demonstrating data persistence.  