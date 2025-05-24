### Black Box Unit Test Cases  

#### Functionality 1. User Registration
- **Step**: Navigate to the Registration Page.  
  **Expectation**: The Registration Page is displayed with fields for username and password.  
- **Step**: Enter a valid username and password and submit the form.  
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

#### Functionality 3. Profile Creation and Update
- **Step**: Login successfully and navigate to the Profile Page.  
  **Expectation**: The Profile Page is displayed with options to create or update the profile.  
- **Step**: Fill in the bio and personal information and save changes.  
  **Expectation**: The profile is updated successfully, and a confirmation message is displayed.  
- **Step**: Leave the bio field empty and attempt to save changes.  
  **Expectation**: An error message is displayed indicating that the bio cannot be empty.

#### Functionality 4. Content Upload and Sharing
- **Step**: Login successfully and navigate to the content upload section.  
  **Expectation**: The content upload form is displayed.  
- **Step**: Upload a valid article and submit.  
  **Expectation**: The article is shared successfully, and a confirmation message is displayed.  
- **Step**: Attempt to upload an article with invalid content (e.g., empty title).  
  **Expectation**: An error message is displayed indicating that the title cannot be empty.

#### Functionality 5. Content Discovery
- **Step**: Login successfully and navigate to the discovery page.  
  **Expectation**: A feed of content shared by other users is displayed.  
- **Step**: Scroll through the feed and click on a shared article.  
  **Expectation**: The article details are displayed correctly.  
- **Step**: Refresh the discovery page after a new article has been uploaded by another user.  
  **Expectation**: The newly uploaded article appears in the feed.

#### Functionality 6. Interacting with Content
- **Step**: Navigate to the discovery page and select an article.  
  **Step**: Click the 'like' button on the article.  
  **Expectation**: The like count for the article increases by one.  
- **Step**: Leave a comment on the article and submit.  
  **Expectation**: The comment is displayed under the article successfully.  
- **Step**: Attempt to like the same article again.  
  **Expectation**: An error message is displayed indicating that the user cannot like the same article multiple times.

#### Functionality 7. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to access the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page with a message indicating that they need to log in.

#### Functionality 8. User Interaction (Follow and Message)
- **Step**: Login successfully and navigate to another user's profile.  
  **Step**: Click the 'Follow' button.  
  **Expectation**: The user is followed successfully, and the button changes to 'Unfollow'.  
- **Step**: Click on the 'Message' button to send a message to the followed user.  
  **Step**: Enter a valid message and submit.  
  **Expectation**: The message is sent successfully, and a confirmation message is displayed.  
- **Step**: Attempt to send an empty message.  
  **Expectation**: An error message is displayed indicating that the message cannot be empty.