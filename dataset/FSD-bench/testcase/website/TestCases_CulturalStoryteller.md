### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password, then submit the registration form.  
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

#### Functionality 3. Explore Stories on the Dashboard Page
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: A collection of stories from various cultures is displayed.  
- **Step**: Click on a story title.  
  **Expectation**: The user is redirected to the Story Details Page for that story.

#### Functionality 4. Search for Stories
- **Step**: Navigate to the Dashboard Page.  
  **Step**: Enter a keyword in the search bar and submit.  
  **Expectation**: A list of stories matching the keyword is displayed.  
- **Step**: Search for stories by cultural origin or category.  
  **Expectation**: The relevant stories are displayed based on the selected criteria.

#### Functionality 5. View Story Details
- **Step**: Click on a story from the Dashboard Page.  
  **Expectation**: The Story Details Page is displayed with the full text and cultural background.  
- **Step**: Check for the presence of a 'Bookmark' button on the Story Details Page.  
  **Expectation**: The 'Add to Bookmarks' button is visible and functional.

#### Functionality 6. Bookmark Stories
- **Step**: Navigate to the Story Details Page of a specific story.  
  **Step**: Click the 'Add to Bookmarks' button.  
  **Expectation**: The story is successfully added to the user's bookmarks, and a confirmation message is displayed.  
- **Step**: Navigate to the Bookmarks Page.  
  **Expectation**: The bookmarked story is listed on the Bookmarks Page.

#### Functionality 7. View and Manage Bookmarked Stories
- **Step**: Navigate to the Bookmarks Page after bookmarking a story.  
  **Expectation**: The list of bookmarked stories is displayed correctly.  
- **Step**: Remove a story from bookmarks.  
  **Expectation**: The story is removed from the bookmarks list, and a confirmation message is displayed.

#### Functionality 8. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.

#### Functionality 9. Local Data Storage
- **Step**: Add a new story to the local storage.  
- **Step**: Refresh the Dashboard Page.  
  **Expectation**: The newly added story appears in the collection on the Dashboard Page.  
- **Step**: Bookmark a story and check the corresponding text file.  
  **Expectation**: The story's details are correctly saved in the bookmarks text file.