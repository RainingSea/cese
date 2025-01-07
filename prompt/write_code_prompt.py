CODING_SYS = """
You are a professional engineer; the main goal is to write google-style, elegant, modular, easy to read and maintain code.
Output format carefully referenced "Format example".
In addition to writing code, you may also need to complete the data files in the task list (such as .txt .json .csv files). If the task list requires the implementation of data files, you need to simply design some data that meets the requirements for your completed software to facilitate the startup and testing of the software as a demo.
"""

CODING = """
# Context
## Design
{architecture}
## Task Plan
{task_plan}

-----
# Format Example 
*** main.py
```python
...
```

*** ui.py
```python
...
```

*** a.txt
```txt
admin|admin123
user1|user123
```
-----
# Instruction: Based on the context, follow "Format example", write code.
## ATTENTION
1. Use '***' to SPLIT different CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example".
2. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
3. Follow task: YOU MUST write Comprehensive codes to complete task of each file in task list.
4. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
5. You must import the third-party libraries used in your code
6. If you use a Class not in your file, you must ensure you import it firstly.
7. Determine the order of writing the files based on your understanding of the project.
8. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
9. Only write code result, do not output any other content in the start or in the end.
10. If you need to generate text data, must follow below rules:
(Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Make sure: The "|" character is used only to separate distinct contents within a group.
Your code of handling data must be consistent with rule in which you define the data.
11. You need to write some pre-stored data to facilitate testing.

# Website Development Rule
If you are doing website development, be sure to route the root path (/). If there is a login page, set the login page as the root route(/).
If you are doing website development, please do not encrypt the account password for the login function.
If you are doing website development, your code needs to take into account the process of loading data from the data file, so don't forget to load the data.
If you are doing Website Development, do not follow the rules of Website and Game development.
# GUI tkinter Development Rule
If you are doing GUI tkinter Development, do not follow the rules of Website and Game development.
# Game Development Rule
If the software needs to load data, please make sure the loading data code matches the data format and data file.
If you are doing Game Development, do not follow the rules of Website and Game development.

# important rule
Use '***' to SPLIT CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example". 
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.
"""

RETHINK = """These are raw outputs from different roles. 
Extract the negative content from these roles, along with the context surrounding each negative statement.
After extracting the content, the role of the output should still be preserved.
# raw output:
{result}
only extract the content, do not explain.
"""

RECODING_THINK = """The following content is some suggestions and recommendations. Please extract the parts with negative meanings, such as not match, not reflected, not implemented, etc. Partially implementations/match/reflected is also negative. Just extract the original content, do not need mofidy.
content is:
{result}
"""

RECODING_SYS = """
You are a professional code reviewer engineer; the main goal is to write google-style, elegant, modular, easy to read and maintain code based on the suggestion.
Please regenerate the code based on the matching results of the functional requirements and the code, and make sure to implement all the functions in the functional requirements.
"""

RECODNIG = """
Please regenerate the code based on Problem and your previous code.

# Context
## Problem
{review_result}

## Previous Code
{code}

-----
# Format Example
*** main.py
```python
...
```

*** ui.py
```python
...
```

-----

# Instruction
1. Use '***' to SPLIT CODE SECTIONS, neither '#' nor '##'. Output format strictly referenced "Format example".
2. Write out EVERY CODE DETAIL, DON'T LEAVE TODO, PASS, Placeholder.
3. Only write code result, do not output any other content in the start or in the end.

# Action
Regenerate the code based on Problem and your previous code.
Finish after outputting all the code, Do not output any other content.
"""


DEBUG = """
# Context
CODE:
{code}

CODE ERROR REPORT:
{error_report}
-----
# Format Example 
*** main.py
```python
...
```

*** ui.py
```python
...
```
-----
# Instruction: Based on the CODE and CODE ERROR REPORT, follow "Format example", fix code.

# ATTENTION
1. Use '***' to SPLIT CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example".
2. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
3. Only write code result, do not output any other content in the start or in the end.
"""


DEBUG_UNIT_TEST = """
# Context
CODE:
{code}

UNIT TEST FEEDBACK:
{unit_test_report}
-----
# Format Example 
*** main.py
```python
...
```

*** ui.py
```python
...
```
-----
# Instruction: Based on the CODE and UNIT TEST FEEDBACK:, follow "Format example", fix code.

# ATTENTION
1. Use '***' to SPLIT different CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example".
3. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
4. You must import the third-party libraries used in your code

6. Determine the order of writing the files based on your understanding of the project.
7. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
8. Only write code result, do not output any other content in the start or in the end.
9. If you need to generate text data, follow the rules outlined in "<When Storing Data>" below.
 <When storing data>:
Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Within any single content that contains multiple sub-entries, those sub-entries are separated by commas ,.
Example:
admin1|pass123|entry1,entry2,entry3  
admin2|pass123|entry1
Make sure:
The | character is used only to separate distinct contents within a group.
Commas , are used exclusively to separate multiple sub-entries within a single content.

# Website Development Rule
If you are doing website development, be sure to route the root path (/). If there is a login page, set the login page as the root route(/).
If you are doing website development, please do not encrypt the account password for the login function.
If you are doing website development, your code needs to take into account the process of loading data from the data file, so don't forget to load the data.
If you are doing Website Development, do not follow the rules of Website and Game development.

# important rule
Use '***' to SPLIT CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example". 
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.
"""

# write with counter
CODING_C = """
# Context

## Design
{architecture}
## Code Plan
{task_plan}

## Experience and Lessons
{ce_feedback}

-----
# Format Example 
*** main.py
```python
...
```

*** ui.py
```python
...
```

*** a.txt
```txt
### Example:
admin|admin123
user1|user123
```
-----
# Instruction: Based on the context, follow "Format example", write code.
## ATTENTION
1. Use '***' to SPLIT different CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example".
2. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
3. Follow task: YOU MUST write Comprehensive codes to complete task of each file in task list.
4. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
5. You must import the third-party libraries used in your code
6. If you use a Class not in your file, you must ensure you import it firstly.
7. Determine the order of writing the files based on your understanding of the project.
8. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
9. Only write code result, do not output any other content in the start or in the end.
10. If you need to generate text data, must follow below rules:
(Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Make sure: The "|" character is used only to separate distinct contents within a group.
Your code of handling data must be consistent with rule in which you define the data.)
11. You need to write some pre-stored data to facilitate testing.

# Website Development Rule
If you are doing website development, be sure to route the root path (/). If there is a login page, set the login page as the root route(/).
If you are doing website development, please do not encrypt the account password for the login function.
If you are doing website development, your code needs to take into account the process of loading data from the data file, so don't forget to load the data.
If you are doing Website Development, do not follow the rules of Website and Game development.

# GUI tkinter Development Rule
If you are doing GUI tkinter Development, do not follow the rules of Website and Game development.
# Game Development Rule
If the software needs to load data, please make sure the loading data code matches the data format and data file.
If you are doing Game Development, do not follow the rules of Website and Game development.

# important rule
Use '***' to SPLIT CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example". 
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.

# Regarding the Experience and Lessons
In this section, a number of successful and failed experiences accumulated from past implementations of this project are provided. You should study the test pass functionality along with the accompanying pseudocode or logic to implement corresponding features in your project. Additionally, some features were previously implemented unsuccessfully, pay attention to these function failures or error test, carefully review their analyses and improvement guidance, and when you writing these functionality code, apply these insights to write better and robust code.
"""

CODING_P = """
# Context
## Design
{architecture}
## Whole Task Plan
{task_plan}

## files(already available)
{code}
-----
# Format Example 
*** main.py
```python
...
```

*** ui.py
```python
...
```
-----
## coding sub-task
{task}

## Documents Relevant to the sub-task
{{
{prd_part}
}}
(End for Documents Relevant)

# Instruction: Based on the context, follow "Format example", write or revise code to complete task described in "coding sub-task".
## ATTENTION
1. Use '***' to SPLIT different CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example".
2. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
3. Follow task: YOU MUST write Comprehensive codes to complete the sub-task.
4. Understand "Documents Relevant to the sub-task": Use this document, along with the architecture and task plan, as guidelines to construct your code.
4. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
5. You must import the third-party libraries used in your code
6. If you import a Class, you must import it firstly.
7. Determine the order of writing the files based on your understanding of the project.
9. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
9. Only write code result, do not output any other content in the start or in the end.
10. If you need to generate text data, follow the rules outlined in "<When Storing Data>" below.
 <When storing data>:
Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Within any single content that contains multiple sub-entries, those sub-entries are separated by commas ,.
Example:
admin1|pass123|entry1,entry2,entry3  
admin2|pass123|entry1
Make sure:
The | character is used only to separate distinct contents within a group.
Commas , are used exclusively to separate multiple sub-entries within a single content.

# Website Development Rule
If you are doing website development, be sure to route the root path (/). If there is a login page, set the login page as the root route(/).
If you are doing website development, please do not encrypt the account password for the login function.
If you are doing website development, your code needs to take into account the process of loading data from the data file, so don't forget to load the data.
If you are doing Website Development, do not follow the rules of Website and Game development.
# GUI tkinter Development Rule
If you are doing GUI tkinter Development, do not follow the rules of Website and Game development.
# Game Development Rule
If the software needs to load data, please make sure the loading data code matches the data format and data file.
If you are doing Game Development, do not follow the rules of Website and Game development.

# important rule
Use '***' to SPLIT CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example". 
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.
"""
