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
  **Expectation**: An error message is displayed indicating that the credentials are incorrect.

#### Functionality 3. Browse News Categories on the Dashboard Page
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: A list of news categories (e.g., politics, sports, entertainment) is displayed.  
- **Step**: Click on a specific news category (e.g., sports).  
  **Expectation**: The user is shown a list of articles related to the selected category.

#### Functionality 4. Search for Specific Topics or Keywords
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: The search bar is visible on the Dashboard Page.  
- **Step**: Enter a specific keyword (e.g., "Olympics") in the search bar and submit.  
  **Expectation**: A list of articles related to the keyword "Olympics" is displayed.  
- **Step**: Enter a keyword that has no related articles.  
  **Expectation**: A message is displayed indicating that no articles were found.

#### Functionality 5. View Article Summaries in the News Feed
- **Step**: Login successfully and navigate to the Dashboard Page.  
  **Expectation**: A list of articles with headlines, summaries, and sources is displayed.  
- **Step**: Click on an article headline.  
  **Expectation**: The user is redirected to the Article Details Page displaying the full text of the article.

#### Functionality 6. User Logout
- **Step**: Logout from the Dashboard Page.  
  **Expectation**: The user is redirected to the Login Page.  
- **Step**: Attempt to navigate back to the Dashboard Page after logging out.  
  **Expectation**: The user is redirected to the Login Page, and access to the Dashboard is denied.