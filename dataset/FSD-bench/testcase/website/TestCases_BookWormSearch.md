### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password, then click the "Register" button.  
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

#### Functionality 3. Book Search
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: The Dashboard Page is displayed with a search bar.  
- **Step**: Enter a valid book title in the search bar and click the "Search" button.  
  **Expectation**: A list of matching book results is displayed with relevant details.  
- **Step**: Enter a keyword that does not match any book titles or authors.  
  **Expectation**: A message is displayed indicating that no results were found.  

#### Functionality 4. View Book Details
- **Step**: Click on a book from the search results on the Dashboard Page.  
  **Expectation**: The Book Details Page for that book is displayed, showing detailed information.  
- **Step**: Check if the Book Details Page contains a description and author details.  
  **Expectation**: The description and author details are displayed correctly.  

#### Functionality 5. Add Book to Reading List
- **Step**: Navigate to the Book Details Page for a specific book.  
  **Step**: Click the "Add to Reading List" button.  
  **Expectation**: The book is added to the user's reading list, and a confirmation message is displayed.  
- **Step**: Navigate to the Reading List Page.  
  **Expectation**: The added book appears in the reading list.  

#### Functionality 6. View and Manage Reading List
- **Step**: Login successfully and navigate to the Reading List Page.  
  **Expectation**: The Reading List Page displays the user's current reading list.  
- **Step**: Remove a book from the reading list.  
  **Expectation**: The book is removed successfully, and the updated reading list is displayed.  

#### Functionality 7. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to navigate back to the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access to the Dashboard is denied.  

#### Functionality 8. Local Data Storage
- **Step**: Add a book to the reading list and then log out.  
- **Step**: Log back in with the same account.  
  **Expectation**: The previously added book appears in the reading list, confirming data persistence.  
- **Step**: Modify the reading list by adding and removing books.  
  **Expectation**: The changes are reflected correctly in the local text files, ensuring data integrity.  