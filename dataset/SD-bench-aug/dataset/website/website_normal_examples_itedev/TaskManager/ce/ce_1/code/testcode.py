import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")  # Use valid credentials
        self.assertIn("Task Manager", self.driver.title)  # Check if redirected to home page

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()
        time.sleep(1)  # Wait for redirection to login page

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Test viewing task list after logging in
        self.login("admin", "admin123")  # Use valid credentials
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')  # Get the list of tasks
        self.assertGreater(len(tasks), 0, "No tasks found.")  # Check if tasks are displayed

    def test_add_new_task(self):
        # Test adding a new task
        self.login("admin", "admin123")  # Use valid credentials
        self.driver.find_element(By.NAME, 'task_description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        # Verify the new task is displayed in the task list
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("New Task", [task.text for task in tasks])

    def test_remove_task(self):
        # Test removing a task
        self.login("admin", "admin123")  # Use valid credentials
        self.driver.find_element(By.NAME, 'task_description').send_keys("Task to Remove")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        # Now remove the task
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        if tasks:
            self.driver.find_element(By.XPATH, '//li[contains(text(), "Task to Remove")]/form/button').click()
            time.sleep(1)  # Wait for the task to be removed

            # Verify the task is no longer in the task list
            tasks = self.driver.find_elements(By.TAG_NAME, 'li')
            self.assertNotIn("Task to Remove", [task.text for task in tasks])

    def test_navigate_back_to_login(self):
        # Test navigation back to login page
        self.login("admin", "admin123")  # Use valid credentials
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for redirection to login page

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_invalid_access(self):
        # Test access to home page without logging in
        self.driver.get('http://localhost:5000/home')
        time.sleep(1)  # Wait for redirection
        self.assertIn("Login", self.driver.title)  # Should redirect to login page

    def test_session_management(self):
        # Test session management by logging in and closing the browser
        self.login("admin", "admin123")  # Use valid credentials
        self.driver.quit()  # Close the browser

        # Start a new session and try to access home page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/home')
        time.sleep(1)  # Wait for redirection
        self.assertIn("Login", self.driver.title)  # Should redirect to login page

if __name__ == '__main__':
    unittest.main()
