import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\codebase\\TaskManager\\ce\\ce_0\\code')
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8494/')  # Open the login page

    def tearDown(self):
        # Close the web driver session and stop the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Tasks", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_view_task_list(self):
        # Functionalities 3: Test viewing task list after logging in
        self.login("user1", "user123")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("user1", "user123")

        # Add a new task
        self.driver.find_element(By.NAME, 'description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//input[@value="Add Task"]').click()
        time.sleep(1)  # Wait for the task to be added

        # Verify the new task is displayed
        self.assertIn("New Task", self.driver.page_source)

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("user1", "user123")

        # Remove the first task
        self.driver.find_element(By.XPATH, '//input[@value="Remove"]').click()
        time.sleep(1)  # Wait for the task to be removed

        # Verify the task is removed
        self.assertNotIn("Task 1", self.driver.page_source)

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigating back to login
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_task_data_storage(self):
        # Functionalities 7: Test task data storage
        self.login("user1", "user123")

        # Add a new task
        self.driver.find_element(By.NAME, 'description').send_keys("Storage Test Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//input[@value="Add Task"]').click()
        time.sleep(1)  # Wait for the task to be added

        # Verify the task is stored in the file
        with open('tasks_user1.txt', 'r') as f:
            tasks = f.read()
            self.assertIn("Storage Test Task|2023-12-31", tasks)

        # Remove the task
        self.driver.find_element(By.XPATH, '//input[@value="Remove"]').click()
        time.sleep(1)  # Wait for the task to be removed

        # Verify the task is removed from the file
        with open('tasks_user1.txt', 'r') as f:
            tasks = f.read()
            self.assertNotIn("Storage Test Task|2023-12-31", tasks)

    def test_invalid_actions(self):
        # Functionalities 8: Test accessing home page without logging in
        self.driver.get('http://localhost:8494/home')
        time.sleep(1)  # Wait for the redirect

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("user1", "user123")
        self.driver.quit()  # Close the browser without logging out

        # Reopen the browser and try to access the home page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8494/home')
        time.sleep(1)  # Wait for the redirect

        # Verify the session is invalid and the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
