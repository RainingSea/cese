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
        self.driver.get('http://localhost:8426/')  # Access the login page

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
        self.assertIn("Home", self.driver.title)  # Verify that the home page has loaded

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
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tasks), 0, "No tasks found on the home page.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("admin", "admin123")

        task_description = "New Task"
        due_date = "2023-12-31"

        # Fill out the task form
        self.driver.find_element(By.NAME, 'task_description').send_keys(task_description)
        self.driver.find_element(By.NAME, 'due_date').send_keys(due_date)
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)  # Wait for the task to be added

        # Verify that the new task is displayed on the home page
        self.assertIn(task_description, self.driver.page_source)

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("admin", "admin123")

        # Assuming the first task can be removed
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        if tasks:
            task_to_remove = tasks[0].text
            # Click the remove button next to the task (assuming there's a button)
            # This part needs to be adjusted based on the actual HTML structure
            self.driver.find_element(By.XPATH, f'//li[contains(text(), "{task_to_remove}")]/following-sibling::button[text()="Remove"]').click()
            time.sleep(1)  # Wait for the task to be removed

            # Verify that the task is no longer displayed
            self.assertNotIn(task_to_remove, self.driver.page_source)

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigating back to login
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_invalid_access(self):
        # Functionalities 8: Test access to home page without logging in
        self.driver.get('http://localhost:8426/home/admin')
        time.sleep(1)  # Wait for the page to load

        # Verify that the user is redirected back to the login page
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("admin", "admin123")
        self.driver.quit()  # Close the browser

        # Reopen the browser and try to access the home page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8426/home/admin')
        time.sleep(1)  # Wait for the page to load

        # Verify that the user is redirected back to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
