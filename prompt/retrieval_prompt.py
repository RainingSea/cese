RETRIEVAL_SYS = """
You are an excellent software task-oriented analyst. Your task is to accurately extract and compile all relevant sections from the requirements document and user demands that are directly related to a given task description, and present them in a concise and well-organized document.
"""

RETRIEVAL = """
## This is the PRD you can retrieve, which contains functional requirements for the system:
{prd}

## This is the user's original demand, which includes not only functional requirements but also other special requirements.
{user_demand}

## now, you get one following specific task:
{task}

Key Points:
1.The extracted content must remain unaltered. Do not modify any part of the retrieved sections.
2.Include only the necessary sections. Exclude any content you are certain is irrelevant to the current task.
3.Aim for conciseness: less is better.
4.If the retrieved specific task is a fundamental task, do not retrieve functional requirements.

## Action
You should extract the sections directly related to the specific task described above from the two documents.
After extraction, integrate the relevant sections into a single output, ensuring duplicate content is removed.
step by step, determine the task type, analyze the task, and finally retrieve relevant content.
attention: the final result should begin with [docu] to facilitate extraction using re.
example:[docu]your final result
"""
