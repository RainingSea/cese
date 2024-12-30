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

#### Functionality 3. User Profile Management
- **Step**: Login successfully and navigate to the Profile Page.  
  **Expectation**: The user's current profile information is displayed.  
- **Step**: Update the profile with new areas of interest and save changes.  
  **Expectation**: The profile is updated successfully, and a confirmation message is displayed.  
- **Step**: Attempt to update the profile with invalid data (e.g., empty fields).  
  **Expectation**: An error message is displayed indicating that all fields are required.  

#### Functionality 4. Join Study Groups
- **Step**: Login successfully and navigate to the Study Groups Page.  
  **Expectation**: A list of available study groups is displayed.  
- **Step**: Select a study group and click the "Join" button.  
  **Expectation**: The user is successfully added to the study group, and a confirmation message is displayed.  
- **Step**: Attempt to join a study group that is already full.  
  **Expectation**: An error message is displayed indicating that the study group is full.  

#### Functionality 5. Share and Access Educational Resources
- **Step**: Login successfully and navigate to the Resources Page.  
  **Expectation**: A list of shared educational resources is displayed.  
- **Step**: Upload a new educational resource (e.g., an article).  
  **Expectation**: The resource is uploaded successfully, and it appears in the list of resources.  
- **Step**: Attempt to upload a resource with invalid format (e.g., unsupported file type).  
  **Expectation**: An error message is displayed indicating that the file format is not supported.  

#### Functionality 6. Messaging in Study Groups
- **Step**: Login successfully and navigate to a study group.  
  **Expectation**: The study group chat interface is displayed.  
- **Step**: Send a message in the study group chat.  
  **Expectation**: The message is sent successfully and appears in the chat history.  
- **Step**: Attempt to send an empty message.  
  **Expectation**: An error message is displayed indicating that the message cannot be empty.  

#### Functionality 7. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to navigate back to the Dashboard Page after logging out.  
  **Expectation**: The user is redirected back to the Login Page, and access is denied.  

#### Functionality 8. Navigate Back to Dashboard
- **Step**: Navigate to the Profile Page after logging in.  
- **Step**: Click the "Back to Dashboard" button.  
  **Expectation**: The user is redirected back to the Dashboard Page with the user's resources and study groups displayed.  

#### Functionality 9. View Educational Resource Details
- **Step**: Login successfully and navigate to the Resources Page.  
- **Step**: Click on a specific educational resource to view details.  
  **Expectation**: The details of the selected educational resource are displayed correctly.  
- **Step**: Attempt to view details of a resource that has been deleted.  
  **Expectation**: An error message is displayed indicating that the resource is not available.  