RETRIEVAL_SYS = """
You are an excellent software analyst. Your task is to identify all the sections related to a task description from the requirements and user_deman, and compile them into a single document.
"""

RETRIEVAL = """
This is the PRD you can retrieve, which contains functional requirements for the system:
{prd}

This is the user's original demand, which includes not only functional requirements but also other special requirements.
{user_demand}

now, you get one following task:
{task}

Based on these two documents, extract the sections related to the task.
You need to integrate the two sections, including removing duplicate parts and so on.
Attention: extracted result must not alter any part of the content retrieved. 
"""
