CODING_SYS = """
You are a professional engineer; the main goal is to write google-style, elegant, modular, easy to read and maintain code.
Output format carefully referenced "Format example".
In addition to writing code, you may also need to complete the data files in the task list (such as .txt). If the task list requires the implementation of data files, you need to simply design some data that meets the requirements for your completed software to facilitate the startup and testing of the software as a demo.
"""

CODING = """
[1] Context
## Design
{architecture}
## Coding Plan
{task_plan}

-----
[2] Format Example 
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
[3] Instruction: Based on the context, follow "Format example", write code.

## ATTENTION
1. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
2. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
3. You must import the third-party libraries used in your code
4. If you use a Class not in your file, you must ensure you import it firstly.
5. Determine the order of writing the files based on your understanding of the project.
6. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
7. Only write code result, do not output any other content in the start or in the end.
8. If you need to generate text data, must follow below rules:
(Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Make sure: The "|" character is used only to separate distinct contents within a group.
Your code of handling data must be consistent with rule in which you define the data.)
9. if you generate json data, you must change the file extension to .json.
10. You need to write some pre-stored data to facilitate testing.

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
1. Use '***' to SPLIT different CODE SECTIONS. Each code section must start with '***' followed by the file name, then followed by the code block enclosed in ```.
- CORRECT: *** filename.py\n ```python\n...\n```
- INCORRECT: ```python\n*** filename.py\n...\n``` (WRONG ORDER)
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.
If you are doing website development, do not encrypt the account password for the login function.
"""

CODING_FD = """
[1] Context
## Existing Code
{exist_code}

## Experience and Lessons
{ce_feedback}

-----
[2] Format Example 
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
[3] Instruction: Based on the CODE and Experience and Lessons, follow "Format example", update your code.
## ATTENTION
1. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
2. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
3. You must import the third-party libraries used in your code
4. If you use a Class not in your file, you must ensure you import it firstly.
5. Determine the order of writing the files based on your understanding of the project.
6. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
7. Only write code result, do not output any other content in the start or in the end.
8. If you need to generate text data, must follow below rules:
(Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Make sure: The "|" character is used only to separate distinct contents within a group.
Your code of handling data must be consistent with rule in which you define the data.)
9. if you generate json data, you must change the file extension to .json.
10. You need to write some pre-stored data to facilitate testing.

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
1. Use '***' to SPLIT different CODE SECTIONS. Each code section must start with '***' followed by the file name, then followed by the code block enclosed in ```.
- CORRECT: *** filename.py\n ```python\n...\n```
- INCORRECT: ```python\n*** filename.py\n...\n``` (WRONG ORDER)
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.
If you are doing website development, do not encrypt the account password for the login function.

[4] Regarding the Experience and Lessons
In this section, a number of successful or failed experiences accumulated from past implementations of this project are provided. 
Pay attention to all these functions.
For the test pass functionality, you should refer the accompanying pseudocode or logic to implement corresponding features in your project. 
Additionally, some features were previously implemented unsuccessfully, pay attention to these function failures or error test, carefully review their analyses and improvement guidance, and when you writing these functionality code, apply these insights to write better and robust code.
"""

# 第一次生成代码时的prompt，需要加design和plan，后续根据反馈改的就不需要加了
CODING_C = """
[1] Context
## Design
{architecture}
## Coding Plan
{task_plan}

-----
[2] Format Example 
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
[3] Instruction: Based on the context, follow "Format example", write code.
## ATTENTION
1. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
2. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
3. You must import the third-party libraries used in your code
4. If you use a Class not in your file, you must ensure you import it firstly.
5. Determine the order of writing the files based on your understanding of the project.
6. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
7. Only write code result, do not output any other content in the start or in the end.
8. If you need to generate text data, must follow below rules:
(Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Make sure: The "|" character is used only to separate distinct contents within a group.
Your code of handling data must be consistent with rule in which you define the data.)
9. if you generate json data, you must change the file extension to .json.
10. You need to write some pre-stored data to facilitate testing.

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
1. Use '***' to SPLIT different CODE SECTIONS. Each code section must start with '***' followed by the file name, then followed by the code block enclosed in ```.
- CORRECT: *** filename.py\n ```python\n...\n```
- INCORRECT: ```python\n*** filename.py\n...\n``` (WRONG ORDER)
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.
If you are doing website development, do not encrypt the account password for the login function.
"""


# positive feedback generating prompt
CODING_ITE_C1 = """
[1] Context
## Existing Code
{exist_code}

## Experience and Lessons
{ce_feedback}

-----
[2] Format Example 
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
[3] Instruction: Based on the CODE and Experience and Lessons, follow "Format example", update your code.
## ATTENTION
1. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
2. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
3. You must import the third-party libraries used in your code
4. If you use a Class not in your file, you must ensure you import it firstly.
5. Determine the order of writing the files based on your understanding of the project.
6. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
7. Only write code result, do not output any other content in the start or in the end.
8. If you need to generate text data, must follow below rules:
(Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Make sure: The "|" character is used only to separate distinct contents within a group.
Your code of handling data must be consistent with rule in which you define the data.)
9. if you generate json data, you must change the file extension to .json.
10. You need to write some pre-stored data to facilitate testing.

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
1. Use '***' to SPLIT different CODE SECTIONS. Each code section must start with '***' followed by the file name, then followed by the code block enclosed in ```.
- CORRECT: *** filename.py\n ```python\n...\n```
- INCORRECT: ```python\n*** filename.py\n...\n``` (WRONG ORDER)
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.
If you are doing website development, do not encrypt the account password for the login function.

[4] Regarding the Experience and Lessons
In this section, a number of successful experiences accumulated from past implementations of this project are provided. 
Pay attention to all these functions.
For these functions, you need to check whether your code includes them. 
If included, you should verify that the logic in your code matches the pseudocode provided, and if there are inconsistencies, you need to modify your functions according to the corresponding pseudocode.
If not included, you should add them based on these psedocode.
Refine the existing code based on these experiences. You still need to output all of the code files.
"""

# negative feedback generating prompt
CODING_ITE_C2 = """
[1] Context

## Existing Code
{exist_code}

## Experience and Lessons
{ce_feedback}

-----
[2] Format Example 
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
[3] Instruction: Based on the CODE and Experience and Lessons, follow "Format example", update your code.
## ATTENTION in Writing Code
1. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
2. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
3. You must import the third-party libraries used in your code
4. If you use a Class not in your file, you must ensure you import it firstly.
5. Determine the order of writing the files based on your understanding of the project.
6. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
7. Only write code result, do not output any other content in the start or in the end.
8. If you need to generate text data, must follow below rules:
(Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Make sure: The "|" character is used only to separate distinct contents within a group.
Your code of handling data must be consistent with rule in which you define the data.)
9. if you generate json data, you must change the file extension to .json.
10. You need to write some pre-stored data to facilitate testing.

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
1. Use '***' to SPLIT different CODE SECTIONS. Each code section must start with '***' followed by the file name, then followed by the code block enclosed in ```.
- CORRECT: *** filename.py\n ```python\n...\n```
- INCORRECT: ```python\n*** filename.py\n...\n``` (WRONG ORDER)
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.
If you are doing website development, do not encrypt the account password for the login function.

[4] Regarding the Experience and Lessons
In this section, a number of failed experiences accumulated from past implementations of this project are provided. 
Pay attention to all these functions.
These features were previously implemented unsuccessfully, carefully review their analyses and improvement guidance.
Apply these insights to refine Your Existing code, especially the implementation of these functions.
Refine the existing code based on these experiences. You still need to output all of the code files.
"""

# -------- not need any more


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
## Instruction:
Based on the CODE and UNIT TEST FEEDBACK:, follow "Format example", fix code.

## ATTENTION
2. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
3. You must import the third-party libraries used in your code
4. If you use a Class not in your file, you must ensure you import it firstly.
6. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
7. Only write code result, do not output any other content in the start or in the end.
8. If you need to generate text data, must follow below rules:
(Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Make sure: The "|" character is used only to separate distinct contents within a group.
Your code of handling data must be consistent with rule in which you define the data.)
9. if you generate json data, you must change the file extension to .json.
10. You need to write some pre-stored data to facilitate testing.

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
1. Use '***' to SPLIT different CODE SECTIONS. Each code section must start with '***' followed by the file name, then followed by the code block enclosed in ```.
- CORRECT: *** filename.py\n ```python\n...\n```
- INCORRECT: ```python\n*** filename.py\n...\n``` (WRONG ORDER)
Adhere strictly to the task requirements and implement them fully; do not include placeholders or "example" for code that is intended for future implementation.
If you are doing website development, do not encrypt the account password for the login function.

Based on the CODE and UNIT TEST FEEDBACK:, follow "Format example", fix code.
"""

CODING_FORMAT = """
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
# Instruction:


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
11. if you generate json data, you must change the file extension to .json.
12. You need to write some pre-stored data to facilitate testing.

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
If you are doing website development, do not encrypt the account password for the login function.
"""


CODING_PROMPT = """
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
## Instruction: 
{instruction}

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
11. if you generate json data, you must change the file extension to .json.
12. You need to write some pre-stored data to facilitate testing.

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
If you are doing website development, do not encrypt the account password for the login function.
"""
