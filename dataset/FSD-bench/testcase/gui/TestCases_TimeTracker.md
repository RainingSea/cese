### Black Box Unit Test Cases  

#### Functionality 1. Create Tasks  
- **Step**: Open the Time Tracker application.  
- **Step**: Click on the "Create Task" button.  
- **Step**: Enter a valid task name and description.  
  **Expectation**: The task is created successfully, and a confirmation message is displayed.  
- **Step**: Attempt to create a task with an empty name.  
  **Expectation**: An error message is displayed indicating that the task name cannot be empty.  

#### Functionality 2. Set Timers for Tasks  
- **Step**: Select an existing task from the task list.  
- **Step**: Click on the "Set Timer" button and enter a valid duration (e.g., 30 minutes).  
  **Expectation**: The timer is set successfully, and a countdown is displayed.  
- **Step**: Attempt to set a timer with an invalid duration (e.g., negative minutes).  
  **Expectation**: An error message is displayed indicating that the duration must be a positive number.  

#### Functionality 3. Set Alarms for Reminders  
- **Step**: Open the Time Tracker application.  
- **Step**: Click on the "Set Alarm" button.  
- **Step**: Enter a valid time for the alarm and select a task to associate with it.  
  **Expectation**: The alarm is set successfully, and a confirmation message is displayed.  
- **Step**: Attempt to set an alarm for a time that has already passed.  
  **Expectation**: An error message is displayed indicating that the alarm time must be in the future.  

#### Functionality 4. Generate Detailed Reports on Time Allocation  
- **Step**: Navigate to the Reports section of the application.  
- **Step**: Click on the "Generate Report" button for the current week.  
  **Expectation**: A detailed report is generated and displayed, showing time allocation for each task.  
- **Step**: Attempt to generate a report without any recorded tasks.  
  **Expectation**: An error message is displayed indicating that no data is available to generate a report.  

#### Functionality 5. Provide Insights to Improve Time Management  
- **Step**: Navigate to the Insights section of the application after generating a report.  
- **Step**: Click on the "Get Insights" button.  
  **Expectation**: Insights are displayed based on the user's time allocation, highlighting areas for improvement.  
- **Step**: Attempt to get insights without any recorded time data.  
  **Expectation**: An error message is displayed indicating that insights cannot be generated without time data.  