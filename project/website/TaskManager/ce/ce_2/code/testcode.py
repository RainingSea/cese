import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8256/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Functionalities 3: Test viewing task list after logging in
        self.login("user1", "user123")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("user1", "user123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-10-30")
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("New Task", [task.text for task in tasks])

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("user1", "user123")
        tasks_before = self.driver.find_elements(By.TAG_NAME, 'li')
        if tasks_before:
            self.driver.find_element(By.NAME, 'task_index').send_keys(0)  # Remove the first task
            self.driver.find_element(By.NAME, 'remove_task').click()
            time.sleep(1)  # Wait for the task to be removed

            tasks_after = self.driver.find_elements(By.TAG_NAME, 'li')
            self.assertNotIn(tasks_before[0].text, [task.text for task in tasks_after])

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigation back to login
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)

    def test_task_data_storage(self):
        # Functionalities 7: Test task data storage
        self.login("user1", "user123")
        task_description = "Persistent Task"
        due_date = "2023-10-30"

        # Add a new task
        self.driver.find_element(By.NAME, 'task_description').send_keys(task_description)
        self.driver.find_element(By.NAME, 'due_date').send_keys(due_date)
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        # Check if the task is in the local text file
        with open('tasks_user1.txt', 'r') as file:
            tasks = file.readlines()
            self.assertIn(f"{task_description}|{due_date}\n", tasks)

        # Remove the task
        self.driver.find_element(By.NAME, 'task_index').send_keys(0)  # Remove the first task
        self.driver.find_element(By.NAME, 'remove_task').click()
        time.sleep(1)  # Wait for the task to be removed

        # Check if the task is removed from the local text file
        with open('tasks_user1.txt', 'r') as file:
            tasks = file.readlines()
            self.assertNotIn(f"{task_description}|{due_date}\n", tasks)

    def test_invalid_access(self):
        # Functionalities 8: Test access without logging in
        self.driver.get('http://localhost:8256/home')
        time.sleep(1)  # Wait for the redirect
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("user1", "user123")
        self.driver.quit()  # Close the browser
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8256/home')
        time.sleep(1)  # Wait for the redirect
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
