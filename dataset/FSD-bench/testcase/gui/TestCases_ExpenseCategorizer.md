### Black Box Unit Test Cases  

#### Functionality 1. Input Expenses
- **Step**: Open the Expense Categorizer application.  
- **Step**: Navigate to the expense input section.  
- **Step**: Enter a valid expense amount and description.  
  **Expectation**: The expense is successfully recorded, and a confirmation message is displayed.  

- **Step**: Enter an invalid expense amount (e.g., a negative number).  
  **Expectation**: An error message is displayed indicating that the expense amount must be positive.  

#### Functionality 2. Automatic Categorization of Expenses
- **Step**: Input an expense with a description that matches a predefined category (e.g., "Dinner at restaurant").  
  **Expectation**: The application automatically categorizes the expense under "Food".  

- **Step**: Input an expense with a description that does not match any predefined category (e.g., "New shoes").  
- **Step**: Check the categorized expenses.  
  **Expectation**: The application prompts the user to categorize the expense manually or suggests creating a new category.  

#### Functionality 3. Create and Customize Categories
- **Step**: Navigate to the category management section.  
- **Step**: Create a new category called "Health".  
  **Expectation**: The new category "Health" is added to the list of available categories.  

- **Step**: Edit an existing category (e.g., change "Entertainment" to "Leisure").  
  **Expectation**: The category name is updated successfully, and the change is reflected in the categorized expenses.  

#### Functionality 4. Display Categorized Expenses
- **Step**: Input multiple expenses across different categories (e.g., food, transportation, entertainment).  
- **Step**: Navigate to the categorized expenses view.  
  **Expectation**: All expenses are displayed under their respective categories for easy tracking.  

- **Step**: Remove an expense from a category.  
- **Step**: Check the categorized expenses view.  
  **Expectation**: The removed expense no longer appears in the respective category.  

#### Functionality 5. View Detailed Summaries of Expenses by Category
- **Step**: Input several expenses across various categories.  
- **Step**: Navigate to the summary section of the application.  
  **Expectation**: A detailed summary of expenses is displayed, showing total amounts spent in each category.  

- **Step**: Filter the summary by a specific category (e.g., "Food").  
  **Expectation**: The summary displays only the expenses related to the selected category, along with the total amount.  