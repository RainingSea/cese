### Black Box Unit Test Cases  

#### Functionality 1. Store Text Snippets  
- **Step**: Open the Text Snippet Organizer application.  
- **Step**: Click on the "Add Snippet" button.  
- **Step**: Enter a valid text snippet in the input field and click "Save".  
  **Expectation**: The snippet is saved successfully and appears in the list of stored snippets.  

- **Step**: Attempt to save an empty snippet.  
  **Expectation**: An error message is displayed indicating that the snippet cannot be empty.  

#### Functionality 2. Categorize Snippets Based on Tags  
- **Step**: Open the Text Snippet Organizer application.  
- **Step**: Select a previously saved snippet.  
- **Step**: Add tags to the snippet and click "Save Tags".  
  **Expectation**: The tags are saved successfully and are displayed alongside the snippet.  

- **Step**: Attempt to add a tag that exceeds the character limit.  
  **Expectation**: An error message is displayed indicating that the tag is too long.  

#### Functionality 3. Add Descriptions to Improve Searchability  
- **Step**: Open the Text Snippet Organizer application.  
- **Step**: Select a previously saved snippet.  
- **Step**: Enter a description in the description field and click "Save Description".  
  **Expectation**: The description is saved successfully and is displayed with the snippet.  

- **Step**: Attempt to save a description that is too long.  
  **Expectation**: An error message is displayed indicating that the description exceeds the allowed length.  

#### Functionality 4. Support Text Formatting for Readability  
- **Step**: Open the Text Snippet Organizer application.  
- **Step**: Select a previously saved snippet.  
- **Step**: Apply bold formatting to a portion of the text and click "Save".  
  **Expectation**: The text is saved with the bold formatting applied and displays correctly.  

- **Step**: Attempt to apply unsupported formatting (e.g., underline in a non-supported format).  
  **Expectation**: An error message is displayed indicating that the formatting is not supported.  

#### Functionality 5. Support Syntax Highlighting  
- **Step**: Open the Text Snippet Organizer application.  
- **Step**: Add a code snippet in a supported programming language and click "Save".  
  **Expectation**: The code snippet is saved with appropriate syntax highlighting applied.  

- **Step**: Open a previously saved code snippet and change the programming language.  
- **Step**: Click "Save".  
  **Expectation**: The syntax highlighting updates to reflect the new programming language.  