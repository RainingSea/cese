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
  **Expectation**: An error message is displayed indicating that the credentials are incorrect.

#### Functionality 3. Search for Specific Words or Phrases
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: The search bar is displayed for entering search queries.  
- **Step**: Enter a specific word or phrase in the search bar and submit.  
  **Expectation**: A list of matching results is displayed with relevant book details such as title, author, summary, and cover image.  
- **Step**: Enter a word or phrase that does not exist in the collection.  
  **Expectation**: A message is displayed indicating that no results were found.

#### Functionality 4. View Book Details
- **Step**: Click on a book from the search results on the Dashboard Page.  
  **Expectation**: The Book Details Page is displayed with detailed information about the selected book.  
- **Step**: Verify that the Book Details Page includes a detailed description and relevant context.  
  **Expectation**: The detailed description and relevant context are correctly displayed.

#### Functionality 5. Add Books to Reading List
- **Step**: Navigate to the Book Details Page of a specific book.  
  **Step**: Click the 'Add to Reading List' button.  
  **Expectation**: The book is added to the user's reading list, and a confirmation message is displayed.  
- **Step**: Navigate to the Reading List Page.  
  **Expectation**: The added book appears in the reading list with correct details.

#### Functionality 6. View and Manage Reading List
- **Step**: Login successfully and navigate to the Reading List Page.  
  **Expectation**: The user's reading list is displayed with all added books.  
- **Step**: Remove a book from the reading list.  
  **Expectation**: The book is removed successfully, and the updated reading list is displayed.

#### Functionality 7. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.

#### Functionality 8. Navigate Back to Dashboard
- **Step**: Navigate to the Book Details Page.  
  **Step**: Click the back button to return to the Dashboard Page.  
  **Expectation**: The user is redirected back to the Dashboard Page with the search results shown.  

#### Functionality 9. View Detailed Information
- **Step**: Click the 'Details' button for a specific book on the Dashboard Page.  
- **Step**: Verify that the detailed information for that book is displayed.  
  **Expectation**: The specific book's details are shown, including title, author, summary, and cover image.  