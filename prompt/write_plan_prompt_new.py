WRITE_PLAN_SYS = """
You are a Project Manager, your goal is break down tasks according to functional requirement/architecture, generate a task plan, and analyze task dependencies to start with the prerequisite modules. the constraint is use same language as user requirement. 
"""

WRITE_PLAN = """
## Context
functional requirement:
{functional_requirement}

architecture:
{software_architecture}
-----

## format example
[CONTENT]

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
        "Contains Game class and ... functions"
    ],
    [
        "main.py",
        "Contains main function, from game import Game"
    ]
],
"Task list": [
    "game.py",
    "main.py"
],
"Shared Knowledge": "`game.py` contains functions shared across the project.",

[/CONTENT]

## nodes: "<node>: <type>  # <instruction>"
- Required packages: typing.List[str]  # Provide required packages in requirements.txt format.
- Required Other language third-party packages: typing.List[str]  # List down the required packages for languages other than Python.
- Logic Analysis: typing.List[typing.List[str]]  # Provide a list of files with the classes/methods/functions to be implemented, including dependency analysis and imports.
- Task list: typing.List[str]  # Break down the tasks into a list of filenames, prioritized by dependency order.
- Full API spec: <class 'str'>  # Describe all APIs using OpenAPI 3.0 spec that may be used by both frontend and backend. If front-end and back-end communication is not required, leave it blank.
- Shared Knowledge: <class 'str'>  # Detail any shared knowledge, like common utility functions or configuration variables.

## constraint
Language: Please use the same language as Human INPUT.
Format: output wrapped inside [CONTENT][/CONTENT] like format example, nothing else.
If you are doing website development, please do not encrypt the account password for the login function.

## action
Follow instructions of nodes, generate output and make sure it follows the format example.
"""

WRITE_PLAN_WITH_FDBACK = """
## Context
functional requirement:
{functional_requirement}

architecture:
{architecture}

## lessons and experience
{ce_feedback}
-----

## format example
[CONTENT]

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
        "Contains Game class and ... functions"
    ],
    [
        "main.py",
        "Contains main function, from game import Game"
    ]
],
"Task list": [
    "game.py",
    "main.py"
],
"Shared Knowledge": "`game.py` contains functions shared across the project.",

[/CONTENT]

## nodes: "<node>: <type>  # <instruction>"
- Required packages: typing.List[str]  # Provide required packages in requirements.txt format.
- Required Other language third-party packages: typing.List[str]  # List down the required packages for languages other than Python.
- Logic Analysis: typing.List[typing.List[str]]  # Provide a list of files with the classes/methods/functions to be implemented, including dependency analysis and imports.
- Task list: typing.List[str]  # Break down the tasks into a list of filenames, prioritized by dependency order.
- Full API spec: <class 'str'>  # Describe all APIs using OpenAPI 3.0 spec that may be used by both frontend and backend. If front-end and back-end communication is not required, leave it blank.
- Shared Knowledge: <class 'str'>  # Detail any shared knowledge, like common utility functions or configuration variables.

## constraint
Language: Please use the same language as Human INPUT.
Format: output wrapped inside [CONTENT][/CONTENT] like format example, nothing else.
If you are doing website development, please do not encrypt the account password for the login function.

## Attention
In "lessons and experience" section, there is a summary and feedback from previous work on this project. When you generate, you need to take these insight into consideration. 
for example, if they are suggestions, you should adopt them. If they are error warnings, you need to avoid them.
However, your main task remains to generate a corresponding code plan based on "original_requirement" and "architecture".

## action
Follow instructions of nodes and Attention, generate output and make sure it follows the format example.
"""


WRITE_PLAN_FORMAT = """
## Context
functional requirement:
{functional_requirement}

architecture:
{software_architecture}
-----

## format example
[CONTENT]
"Required packages": ,

"Required Other language third-party packages":,

"Logic Analysis": Provide a list of files with the classes/methods/functions to be implemented, with needed description.

"Task list": [
    "filename",
    "filename",
    ...
],

"Shared Knowledge": ,
[/CONTENT]

## <instruction>


## constraint
Language: Please use the same language as Human INPUT.
Format: output wrapped inside [CONTENT][/CONTENT] like format example, nothing else.
If you are doing website development, please do not encrypt the account password for the login function.
---
"""

WRITE_PLAN_PROMPT = """
## Context
functional requirement:
{functional_requirement}

architecture:
{software_architecture}
-----

## format example
[CONTENT]
"Required packages": ,

"Required Other language third-party packages":,

"Logic Analysis": Provide a list of files with the classes/methods/functions to be implemented, with needed description.

"Task list": [
    "filename",
    "filename",
    ...
],

"Shared Knowledge": ,
[/CONTENT]

## <instruction>
{instruction}

## constraint
Language: Please use the same language as Human INPUT.
Format: output wrapped inside [CONTENT][/CONTENT] like format example, nothing else.
If you are doing website development, please do not encrypt the account password for the login function.
Specially, do not use flask_wtf to build html files.

## action
Follow instructions, generate output and make sure it follows the format example.
"""

WRITE_PLAN_WITH_FDBACK_META = """
## Context
functional requirement:
{functional_requirement}

architecture:
{software_architecture}

## lessons and experience
{ce_feedback}
-----

## format example
[CONTENT]
"Required packages": ,

"Required Other language third-party packages":,

"Logic Analysis": Provide a list of files with the classes/methods/functions to be implemented, with needed description.

"Task list": [
    "filename",
    "filename",
    ...
],

"Shared Knowledge": ,
[/CONTENT]

## <instruction>
{instruction}

## constraint
Language: Please use the same language as Human INPUT.
Format: output wrapped inside [CONTENT][/CONTENT] like format example, nothing else.
If you are doing website development, please do not encrypt the account password for the login function.
Specially, do not use flask_wtf to build html files.

## Attention
In "lessons and experience" section, there is a summary and feedback from previous work on this project. When you generate, you need to take these insight into consideration. 
for example, if they are suggestions or good strength, you should adopt them. If they are error warnings, you need to avoid them.
However, your main task remains to generate a corresponding code plan based on "original_requirement" and "architecture".

## Action
Follow instructions of nodes and Attention, generate output and make sure it follows the format example.
"""
