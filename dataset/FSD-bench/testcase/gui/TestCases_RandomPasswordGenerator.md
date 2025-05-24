### Black Box Unit Test Cases  

#### Functionality 1. Specify Desired Password Length
- **Step**: Open the Random Password Generator application.  
- **Step**: Enter a valid password length (e.g., 12) in the designated input field.  
  **Expectation**: The application accepts the input and displays the specified length in the interface.  
- **Step**: Enter an invalid password length (e.g., -5 or 0).  
  **Expectation**: The application shows an error message indicating that the length must be a positive integer.

#### Functionality 2. Select Inclusion/Exclusion of Character Types
- **Step**: Open the Random Password Generator application.  
- **Step**: Check the boxes for uppercase letters, lowercase letters, numbers, and symbols.  
  **Expectation**: The application reflects the selected options in the password generation settings.  
- **Step**: Uncheck all character type options and attempt to generate a password.  
  **Expectation**: The application shows an error message indicating that at least one character type must be selected.

#### Functionality 3. Exclude Ambiguous Characters
- **Step**: Open the Random Password Generator application.  
- **Step**: Select the option to exclude ambiguous characters (e.g., 'l', '1', 'O', '0').  
  **Expectation**: The application indicates that ambiguous characters will be excluded from the generated password.  
- **Step**: Generate a password with the ambiguous characters excluded.  
  **Expectation**: The generated password does not contain any ambiguous characters.

#### Functionality 4. Generate Random Password
- **Step**: Open the Random Password Generator application.  
- **Step**: Specify a password length of 10 and select uppercase letters, lowercase letters, and numbers.  
- **Step**: Click the "Generate Password" button.  
  **Expectation**: A random password is generated that meets the specified criteria (length and character types).  
- **Step**: Generate a password with a length of 15 and all character types selected, including symbols.  
  **Expectation**: A random password is generated that meets the specified criteria and includes symbols.  

#### Functionality 5. Save Generated Password to Local Text File
- **Step**: Generate a random password using the application.  
- **Step**: Click the "Save Password" button.  
  **Expectation**: The application prompts for a file name and saves the generated password to a local text file.  
- **Step**: Open the saved text file.  
  **Expectation**: The generated password is correctly saved in the text file.