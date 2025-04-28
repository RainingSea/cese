import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the server and initialize the webdriver
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Check if redirected to home page

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
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Functionalities 3: Test viewing task list after logging in
        self.login("admin", "admin123")
        self.assertIn("Your Tasks", self.driver.page_source)  # Check if task list is visible

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("admin", "admin123")
        self.driver.find_element(By.ID, 'description').send_keys("New Task")
        self.driver.find_element(By.ID, 'due_date').send_keys("2023-10-31")
        self.driver.find_element(By.XPATH, '//input[@value="Add Task"]').click()
        time.sleep(1)  # Wait for the task to be added

        # Verify that the new task appears in the task list
        self.assertIn("New Task", self.driver.page_source)

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("admin", "admin123")
        # Assuming there is a remove button next to tasks, we will need to find it
        # This is a placeholder as the actual implementation of removing tasks is not provided
        self.fail("Remove task functionality is not implemented in the codebase.")

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigation back to login page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Back to Login').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)

    def test_invalid_access(self):
        # Functionalities 8: Test access to home page without logging in
        self.driver.get('http://localhost:8080/home')
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)  # Should redirect to login page

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("admin", "admin123")
        self.driver.quit()  # Close the browser
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080/home')
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)  # Should redirect to login page

if __name__ == '__main__':
    unittest.main()
