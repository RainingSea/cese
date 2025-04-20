from openai import OpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

inputs = """You are a professional engineer; the main goal is to write google-style, elegant, modular, easy to read and maintain code.
Output format carefully referenced "Format example".
In addition to writing code, you may also need to complete the data files in the task list (such as .txt). If the task list requires the implementation of data files, you need to simply design some data that meets the requirements for your completed software to facilitate the startup and testing of the software as a demo.

[1] Context
## Functional Requirements
[OUTPUT]
## general overview of the project
Develop a web application named 'Medical Info Tracker' that helps users track and manage medical information, including diagnoses, medications, treatments, and appointment reminders.
## software functional requirements
1. **User Registration**
   - The system shall provide a Registration Page where users can create an account by entering a username and password.
2. **User Login**
   - The system shall provide a Login Page where users can log in to their account by entering their username and password.
3. **Medical Information Management**
   - The system shall allow users to input and manage their medical information, including:
     - Diagnoses
     - Medications
     - Treatments
4. **Appointment Reminders**
   - The system shall allow users to set appointment reminders and send notifications to users when appointments are due.
5. **Medical History Viewing and Editing**
   - The system shall enable users to view and edit their medical history.
   - The system shall allow users to track their progress over time.
6. **User Logout**
   - The system shall provide a logout functionality that allows users to log out of their account, returning them to the Login Page.
[/OUTPUT]

## Design
[CONTENT]
"Implementation approach": "We will use Flask as the web framework to handle routing and server-side logic, allowing for rapid development of the web application. The application will be structured to include user registration, login, and management of medical information. We will utilize local text files for data storage, ensuring that different types of data are stored in separate `.txt` files for easy access and management.",
"UI design": "- The main UI will consist of a simple navigation bar with links to the Registration Page, Login Page, and Dashboard. Each page will have forms for user input and display relevant information. The Dashboard will allow users to view and manage their medical information and appointment reminders.",
"Data Storage": "Data will be stored in local text files. Different types of data will be stored in separate files. The following files will be created: `users.txt` for user credentials, `medical_info.txt` for medical records, and `appointments.txt` for appointment reminders. Each file will be structured with one entry per line, using a simple delimiter to separate fields.",
"File list": ["main.py", "templates/login.html", "templates/registration.html", "templates/dashboard.html", "users.txt", "medical_info.txt", "appointments.txt"],
"Data structures and interfaces": "
classDiagram
    class UserManager {
        -users: dict
        +__init__()
        +register(username: str, password: str) -> bool
        +login(username: str, password: str) -> bool
        +load_users() -> None
        +save_users() -> None
    }
    class MedicalInfoManager {
        -medical_info: list
        +__init__()
        +add_medical_info(user: str, info: str) -> None
        +edit_medical_info(user: str, index: int, new_info: str) -> None
        +delete_medical_info(user: str, index: int) -> None
        +load_medical_info(user: str) -> list
        +save_medical_info(user: str) -> None
    }
    class AppointmentManager {
        -appointments: list
        +__init__()
        +add_appointment(user: str, appointment: str) -> None
        +edit_appointment(user: str, index: int, new_appointment: str) -> None
        +delete_appointment(user: str, index: int) -> None
        +load_appointments(user: str) -> list
        +save_appointments(user: str) -> None
    }
    class App {
        -user_manager: UserManager
        -medical_info_manager: MedicalInfoManager
        -appointment_manager: AppointmentManager
        +run() -> None
    }
    UserManager --> MedicalInfoManager
    UserManager --> AppointmentManager
    MedicalInfoManager --> AppointmentManager
    App --> UserManager
    App --> MedicalInfoManager
    App --> AppointmentManager
",
[/CONTENT]

-----
[2]Format Example 
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
1. Use '***' to SPLIT different CODE SECTIONS. do not forget ``` in each file, refer the the example. Output format carefully referenced "Format example".
2. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
3. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THE FILE.
4. You must import the third-party libraries used in your code
5. If you use a Class not in your file, you must ensure you import it firstly.
6. Determine the order of writing the files based on your understanding of the project.
7. Write out EVERY CODE DETAIL, DON'T LEAVE TODO,PASS,PLACEHOLDER.
8. Only write code result, do not output any other content in the start or in the end.
9. If you need to generate text data, must follow below rules:
(Different groups of data are distinguished by line breaks.
Different contents of the same group of data are distinguished by |.
Make sure: The "|" character is used only to separate distinct contents within a group.
Your code of handling data must be consistent with rule in which you define the data.)
10. if you generate json data, you must change the file extension to .json.
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
If you are doing website development, do not encrypt the account password for the login function.

[4] Regarding the Experience and Lessons
In this section, a number of successful or failed experiences accumulated from past implementations of this project are provided. 
Pay attention to all these functions.
For the test pass functionality, you should refer the accompanying pseudocode or logic to implement corresponding features in your project. 
Additionally, some features were previously implemented unsuccessfully, pay attention to these function failures or error test, carefully review their analyses and improvement guidance, and when you writing these functionality code, apply these insights to write better and robust code.
"""


def chat_to_LLM(messages):

    client = OpenAI(
        api_key="sk-JQiygLRku49PwPTtPTax1mcy97OFAlO4EagYvHWlCVBVTUmC",  # 只需要填写key就可以了
        base_url="https://api.chatanywhere.tech",
    )
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        top_p=0.1,
        seed=42,
        # stream=True, # 这个开了要用chunk的调用方法
    )
    # print(response.choices[0].message.content, end="", flush=True)
    return response.choices[0].message.content


def chat_to_LLM_langchain():
    a = HumanMessage(content="Hello!")
    model = ChatOpenAI(
        model="gpt-4o-mini",
        api_key="sk-JQiygLRku49PwPTtPTax1mcy97OFAlO4EagYvHWlCVBVTUmC",
        base_url="https://api.chatanywhere.tech",
        model_kwargs={"top_p": 1.2},
    )
    print(model.invoke([a]))


if __name__ == "__main__":
    messages = [{"role": "user", "content": inputs}]
    print(chat_to_LLM(messages))

    # chat_to_LLM_langchain()
