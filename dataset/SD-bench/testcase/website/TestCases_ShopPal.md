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
  **Expectation**: An error message is displayed indicating that the login credentials are incorrect.

#### Functionality 3. Create Personalized Collections
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: The Dashboard Page is displayed with options to create collections.  
- **Step**: Create a new collection by entering a collection name and saving it.  
  **Expectation**: The new collection appears in the user's list of collections.  
- **Step**: Attempt to create a collection with an empty name.  
  **Expectation**: An error message is displayed indicating that the collection name cannot be empty.

#### Functionality 4. Track Price Changes
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Step**: Add a product to a collection and enable price tracking.  
  **Expectation**: The product is saved with price tracking enabled.  
- **Step**: Simulate a price change for the tracked product.  
  **Expectation**: The application updates the price change information accordingly.

#### Functionality 5. View Detailed Product Information
- **Step**: Search for a product using keywords on the Dashboard Page.  
  **Expectation**: A list of products matching the search criteria is displayed.  
- **Step**: Click on a product to view its detailed information.  
  **Expectation**: The detailed product information, including description, reviews, and pricing, is displayed.

#### Functionality 6. Search for Products
- **Step**: Navigate to the search bar on the Dashboard Page.  
  **Step**: Enter a keyword related to a product and submit the search.  
  **Expectation**: A list of products related to the keyword is displayed.  
- **Step**: Search for a product by category.  
  **Expectation**: The application displays products that belong to the selected category.

#### Functionality 7. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.

#### Functionality 8. Navigate Back to Dashboard
- **Step**: Click on a product to view its detailed information.  
- **Step**: Click the back button to return to the Dashboard Page.  
  **Expectation**: The user is redirected back to the Dashboard Page with the product list shown.

#### Functionality 9. Receive Notifications for Discounts
- **Step**: Login successfully and navigate to a product in a collection.  
  **Step**: Enable notifications for price drops on that product.  
  **Expectation**: The application confirms that notifications are enabled for that product.  
- **Step**: Simulate a discount on the tracked product.  
  **Expectation**: The user receives a notification about the discount via the application.