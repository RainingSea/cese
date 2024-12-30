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
  **Expectation**: An error message is displayed indicating invalid credentials.

#### Functionality 3. Create and Upload Travel Albums
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: The user can see an option to create a new travel album.  
- **Step**: Click on "Create Album", fill in the album details, and upload images.  
  **Expectation**: The album is created successfully, and a confirmation message is displayed.  
- **Step**: Attempt to create an album without filling in required fields.  
  **Expectation**: An error message is displayed indicating that all required fields must be filled.

#### Functionality 4. Customize Album Layout and Design
- **Step**: Navigate to an existing album.  
  **Expectation**: The album is displayed with customization options.  
- **Step**: Change the layout and design of the album and save changes.  
  **Expectation**: The album reflects the new layout and design upon refresh.  
- **Step**: Attempt to customize the album without being logged in.  
  **Expectation**: The user is redirected to the Login Page.

#### Functionality 5. Share Albums
- **Step**: Navigate to an existing album.  
  **Expectation**: The album is displayed with sharing options.  
- **Step**: Select the option to share the album publicly.  
  **Expectation**: The album is shared publicly, and a confirmation message is displayed.  
- **Step**: Attempt to share an album without having permission.  
  **Expectation**: An error message is displayed indicating insufficient permissions.

#### Functionality 6. Explore and View Albums Shared by Others
- **Step**: Navigate to the Explore Page.  
  **Expectation**: A list of albums shared by other users is displayed.  
- **Step**: Click on an album to view its details.  
  **Expectation**: The album details are displayed, including images and comments.  
- **Step**: Attempt to view an album that has been set to private.  
  **Expectation**: An error message is displayed indicating that the album is private.

#### Functionality 7. Interact with Other Users
- **Step**: Navigate to an album shared by another user.  
  **Expectation**: The album is displayed with options to like and comment.  
- **Step**: Click the "Like" button on the album.  
  **Expectation**: The like is registered, and the like count is updated.  
- **Step**: Attempt to comment on an album without being logged in.  
  **Expectation**: The user is redirected to the Login Page.

#### Functionality 8. Follow Other Users
- **Step**: Navigate to a user's profile page.  
  **Expectation**: The user's profile is displayed with a "Follow" button.  
- **Step**: Click the "Follow" button.  
  **Expectation**: The user is followed successfully, and a confirmation message is displayed.  
- **Step**: Attempt to follow the same user again.  
  **Expectation**: An error message is displayed indicating that the user is already being followed.

#### Functionality 9. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected to the Login Page.  

#### Functionality 10. Receive Updates on New Albums
- **Step**: Follow another user and log out.  
  **Expectation**: The user is logged out successfully.  
- **Step**: Log back in and navigate to the Dashboard Page.  
  **Expectation**: The user receives notifications about new albums from followed users.  
- **Step**: Click on a notification.  
  **Expectation**: The user is redirected to the new album shared by the followed user.