WRITE_PLAN_SYS = """
You are a Project Manager, your goal is break down tasks according to functional requirement/architecture, generate a task plan, and analyze task dependencies to start with the prerequisite modules. the constraint is use same language as user requirement. 
"""

WRITE_PLAN = """
## Context
functional requirement:
{functional_requirement}

architecture:
{architecture}
-----

## format example
{{
"Required packages": [
    "flask==1.1.2",
    "bcrypt==3.2.0"
],
"Required Other language third-party packages": [
    "No third-party dependencies required"
],
"Logic Analysis": [
    [
        "game.py",
        "The main file of the game, responsible for initializing the game window.... Contains Game class and ... functions"
    ],
    [
        "main.py",
        "Contains main function and the main frame, import Game, Logic..."
    ]
],
"Task list": 
{{
    'T0':'|Initialize the game window,
    'T1':'|complete the moving logic,
    'T2':'|determine the data structure,
    'T3':'|complete the storage,
    ...
}},
"Shared Knowledge": "`game.py` contains functions shared across the project.",
}}

## nodes: "<node>: <type>  # <instruction>"
- Required packages: typing.List[str]  # Provide required packages in requirements.txt format.
- Required Other language third-party packages: typing.List[str]  # List down the required packages for languages other than Python.
- Logic Analysis: typing.List[typing.List[str]]  # Provide a list of files with the classes/methods/functions to be implemented, including dependency analysis and imports.
- Task list: typing.Dict[str]  # Break down the project development into many subtasks(in a dictionary format), each sub-task completes a portion of closely related requirements:
(1)its name(T0,T1...)
(2)the functionalities that need to be completed for this task.
use | to seperate thesse part as example. must no circles in the dependency tasks. related files must from file list in architecture.
You can break down the work into several tasks to tackle more challenging functionalities.
The decomposed tasks only include development-related tasks; higher-level work such as testing, security, and maintenance is not required for now.
- Full API spec: <class 'str'>  # Describe all APIs using OpenAPI 3.0 spec that may be used by both frontend and backend. If front-end and back-end communication is not required, leave it blank.
- Shared Knowledge: <class 'str'>  # Detail any shared knowledge, like common utility functions or configuration variables.

## constraint
Language: Please use the same language as Human INPUT.
Format: output like format example, nothing else.
If you are doing website development, please do not encrypt the account password for the login function.
Related and simple tasks should be combined into one task to reduce the overall number of tasks(no more than 7) during you making "Task List".

## action
Follow instructions of nodes, generate output and make sure it follows the format example.
"""
