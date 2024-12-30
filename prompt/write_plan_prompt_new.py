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
        "The main file of the game, responsible for initializing the game.... Contains Game class and ... functions"
    ],
    [
        "main.py",
        "Contains main function and the main frame, import Game, Logic..."
    ]
],
"Task list": 
{{
    'T0':'|Initialize the game window.|implement XXX Class to create window, implement XXX functions to load game...|[]|related files:["game.py"]',
    'T1':'|complete the moving logic |complete the XXX function, implement relevant code in ui...|[T0]|related files:[main.py,game.py]',
    'T2':'|complete the moving logic |continue to implement XXX function and XXX object, record the moving. for ui, do... |[T0]|related files:[main.py]',
    'T3':'|complete the storage |based on the game logic, record the score and other data, and... |[T0]|related files:[main.py,game.py]',
    ...
}},
"Shared Knowledge": "`game.py` contains functions shared across the project.",
}}

## nodes: "<node>: <type>  # <instruction>"
- Required packages: typing.List[str]  # Provide required packages in requirements.txt format.
- Required Other language third-party packages: typing.List[str]  # List down the required packages for languages other than Python.
- Logic Analysis: typing.List[typing.List[str]]  # Provide a list of files with the classes/methods/functions to be implemented, including dependency analysis and imports.
- Task list: typing.Dict[str]  # Break down the tasks into a subtasks-node-graph(in a dictionary format), each node contains:
(1)its name(T0,T1...)
(2)its role in the project construction[hign level summary, such as what user story the sub-task is reponsible for, and others]
(3)detailed task description, instructing the coder what to do.
(4)its dependency tasks.
(5)related files, use | to seperate thesse part as example. must no circles in the dependency tasks. related files must from file list in architecture.
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
