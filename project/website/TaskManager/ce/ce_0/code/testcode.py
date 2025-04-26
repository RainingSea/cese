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
        self.driver.get('http://localhost:8254/')  # Access the login page

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

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Verify that the home page has loaded

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
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
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')  # Get task list items
        self.assertGreater(len(tasks), 0, "No tasks found on the home page.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("admin", "admin123")
        
        # Add a new task
        self.driver.find_element(By.NAME, 'description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-10-10")
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        # Verify that the new task appears in the task list
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("New Task", [task.text for task in tasks])

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("admin", "admin123")
        
        # Remove the first task
        self.driver.find_element(By.XPATH, '//form[1]//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the task to be removed

        # Verify that the task is no longer in the task list
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertNotIn("Task 1", [task.text for task in tasks])

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigation back to login
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_invalid_access(self):
        # Functionalities 8: Test access to home page without logging in
        self.driver.get('http://localhost:8254/home')
        time.sleep(1)  # Wait for the redirect

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("admin", "admin123")
        self.driver.quit()  # Close the browser

        # Reopen the browser and try to access the home page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8254/home')
        time.sleep(1)  # Wait for the redirect

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
