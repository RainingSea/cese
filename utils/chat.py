from openai import OpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

inputs = """You are a professional engineer; the main goal is to write google-style, elegant, modular, easy to read and maintain code.
Output format carefully referenced "Format example".
In addition to writing code, you may also need to complete the data files in the task list (such as .txt). If the task list requires the implementation of data files, you need to simply design some data that meets the requirements for your completed software to facilitate the startup and testing of the software as a demo.


[1] Context
## Existing Code
*** main.py
```python
from flask import Flask, render_template, request, redirect, url_for, session
from user_registration import UserManager
from culture_exploration import CultureManager
from bookmark_management import BookmarkManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('user_credentials.txt')
culture_manager = CultureManager('culture_facts.txt')
bookmark_manager = BookmarkManager('user_bookmarks.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    cultures = culture_manager.load_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<culture_name>', methods=['GET'])
def culture_details(culture_name):
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', details=details)

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    if 'username' in session:
        bookmarks = bookmark_manager.load_bookmarks(session['username'])
        return render_template('bookmarks.html', bookmarks=bookmarks)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
```

*** user_registration.py
```python
class UserManager:
    def __init__(self, user_file: str):
        self.user_file = user_file
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.user_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> dict:
        users = {}
        try:
            with open(self.user_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users
```

*** culture_exploration.py
```python
class CultureManager:
    def __init__(self, culture_file: str):
        self.culture_file = culture_file
        self.cultures = self.load_cultures()

    def load_cultures(self) -> dict:
        cultures = {}
        try:
            with open(self.culture_file, 'r') as f:
                for line in f:
                    name, description = line.strip().split('|')
                    cultures[name] = description
        except FileNotFoundError:
            pass
        return cultures

    def get_culture_details(self, culture_name: str) -> str:
        return self.cultures.get(culture_name, "Culture not found.")
```

*** bookmark_management.py
```python
class BookmarkManager:
    def __init__(self, bookmark_file: str):
        self.bookmark_file = bookmark_file

    def add_bookmark(self, username: str, culture_name: str) -> bool:
        bookmarks = self.load_bookmarks(username)
        if culture_name not in bookmarks:
            bookmarks.append(culture_name)
            self.save_bookmarks(username, bookmarks)
            return True
        return False

    def remove_bookmark(self, username: str, culture_name: str) -> bool:
        bookmarks = self.load_bookmarks(username)
        if culture_name in bookmarks:
            bookmarks.remove(culture_name)
            self.save_bookmarks(username, bookmarks)
            return True
        return False

    def load_bookmarks(self, username: str) -> list:
        bookmarks = []
        try:
            with open(self.bookmark_file, 'r') as f:
                for line in f:
                    user, culture = line.strip().split('|')
                    if user == username:
                        bookmarks.append(culture)
        except FileNotFoundError:
            pass
        return bookmarks

    def save_bookmarks(self, username: str, bookmarks: list):
        with open(self.bookmark_file, 'w') as f:
            for culture in bookmarks:
                f.write(f"{username}|{culture}\n")
```

*** templates/registration.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" name="username" required>
        <label for="password">Password:</label>
        <input type="password" name="password" required>
        <button type="submit">Register</button>
    </form>
</body>
</html>
```

*** templates/login.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" name="username" required>
        <label for="password">Password:</label>
        <input type="password" name="password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

*** templates/dashboard.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>
    <h1>Culture Dashboard</h1>
    <ul>
        {% for culture in cultures %}
            <li><a href="{{ url_for('culture_details', culture_name=culture) }}">{{ culture }}</a></li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('bookmarks') }}">My Bookmarks</a>
</body>
</html>
```

*** templates/culture_details.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Culture Details</title>
</head>
<body>
    <h1>Culture Details</h1>
    <p>{{ details }}</p>
    <a href="{{ url_for('dashboard') }}">Back to Dashboard</a>
</body>
</html>
```

*** templates/bookmarks.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Bookmarks</title>
</head>
<body>
    <h1>My Bookmarks</h1>
    <ul>
        {% for bookmark in bookmarks %}
            <li>{{ bookmark }}</li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('dashboard') }}">Back to Dashboard</a>
</body>
</html>
```

*** user_credentials.txt
```txt
admin|admin123
user1|user123
```

*** culture_facts.txt
```txt
Japan|A country known for its rich culture and history.
Brazil|Famous for its carnival festival and Amazon rainforest.
France|Renowned for its art, fashion, and cuisine.
```

*** user_bookmarks.txt
```txt
user1|Japan
user1|France
```

## Experience and Lessons
|Case|:**login**
   ```pseudocode
   FUNCTION UserManager
       FUNCTION login(username, password)
           FOR each user IN users
               IF user[0] == username AND user[1] == password
                   session['username'] = username
                   RETURN True
               ENDIF
           ENDFOR
           RETURN False
   END FUNCTION

   FUNCTION login_page()
       RENDER login.html
   END FUNCTION
   ```
|Case|:**view_bookmarks**
   ```pseudocode
   FUNCTION bookmarks()
       bookmark_manager = NEW BookmarkManager()
       bookmarks = bookmark_manager.get_bookmarks()
       RENDER bookmarks.html with bookmarks
   END FUNCTION
   ```


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
- CORRECT: *** filename.py
 ```python
...
```
- INCORRECT: ```python
*** filename.py
...
``` (WRONG ORDER)
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

# 6938
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
