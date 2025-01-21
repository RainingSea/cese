import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8987/login') 

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Task Manager", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_view_task_list(self):
        # Functionalities 3: Test viewing task list after logging in
        self.login("admin", "admin123")

        # Verify that the Home Page shows tasks
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("admin", "admin123")

        task_description = "New Task"
        due_date = "2023-11-01"

        # Fill out the new task form
        self.driver.find_element(By.NAME, 'task_description').send_keys(task_description)
        self.driver.find_element(By.NAME, 'due_date').send_keys(due_date)
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()

        # Verify that the new task is displayed on the Home Page
        self.assertIn(task_description, self.driver.page_source)

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.fail("Not implemented")

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigating back to login
        self.login("admin", "admin123")

        # Click the Logout link
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.page_source)

    def test_task_data_storage(self):
        # Functionalities 7: Test task data storage
        self.fail("Not implemented")

    def test_invalid_actions(self):
        # Functionalities 8: Test accessing home page without logging in
        self.driver.get('http://localhost:8987/home')

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.page_source)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("admin", "admin123")
        self.driver.quit()

        # Reopen the browser and check if login is required
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8987/home')

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
