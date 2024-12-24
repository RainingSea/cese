# **Black Box Unit Test Cases**

### **Functionalities 1. Enable Text File Creation and Editing**

​	•	**Step**: Create a new text file.

**Expectation**: A blank text file opens for editing without errors.

​	•	**Step**: Open an existing text file.

**Expectation**: The file is loaded, and its content is displayed correctly.

​	•	**Step**: Edit the content of a text file and save it.

**Expectation**: Changes are saved successfully, and the file reflects the updated content.

​	•	**Step**: Attempt to open an unsupported file format (e.g., PDF).

**Expectation**: The software displays an error message indicating the file format is unsupported.



###  **Functionalities 2. Provide Syntax Highlighting for Various Programming Languages**

​	•	**Step**: Open a file with Python code.

**Expectation**: Syntax elements (e.g., keywords, strings, comments) are highlighted in distinct colors.

​	•	**Step**: Change the language setting to JavaScript for a file.

**Expectation**: Syntax highlighting updates to reflect JavaScript rules.



### **Functionalities 3. Offer Code Indentation Features**

​	•	**Step**: Write a block of code with mixed indentation (spaces and tabs) and use the re-indent tool.

**Expectation**: The code is reformatted with consistent indentation.

​	•	**Step**: Press the Tab key to indent a line of code.

**Expectation**: The line is indented by the configured amount (e.g., 4 spaces or 1 tab).

​	•	**Step**: Use the “Unindent” feature on an indented line.

**Expectation**: The line’s indentation is reduced by one level.



### **Functionalities 4. Provide Search Functionality**

​	•	**Step**: Search for a specific word in a text file.

**Expectation**: All occurrences of the word are highlighted, and navigation tools (e.g., “Next,” “Previous”) are available.



### **Functionalities 5. Provide Replace Functionality**

​	•	**Step**: Replace a specific word with another word in a text file.

**Expectation**: All specified instances of the word are replaced successfully.

​	•	**Step**: Perform a “Find and Replace” operation with a regular expression.

**Expectation**: Matches are found based on the regex pattern, and replacements are made accordingly.



### **Functionalities 6. Offer Customizable Themes**

​	•	**Step**: Open the theme customization settings.

**Expectation**: A list of available themes is displayed.

​	•	**Step**: Apply a dark theme.

**Expectation**: The editor updates with the selected dark theme (e.g., dark background, light text).

