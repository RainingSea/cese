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
        self.driver.get('http://localhost:8427/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_registration(self):
        # Functionalities 2: User Registration
        self.driver.get('http://localhost:8427/register')
        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Functionalities 3: View Task List
        self.login("user1", "user123")
        self.assertIn("Your Tasks", self.driver.page_source)

    def test_add_new_task(self):
        # Functionalities 4: Add New Task
        self.login("user1", "user123")
        self.driver.find_element(By.NAME, 'description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-10-30")
        self.driver.find_element(By.NAME, 'add_task').click()

        # Verify the task was added
        self.assertIn("New Task", self.driver.page_source)

    def test_remove_task(self):
        # Functionalities 5: Remove Task
        self.login("user1", "user123")
        self.driver.find_element(By.XPATH, '//button[contains(text(), "Remove Task")]').click()

        # Verify the task was removed
        self.assertNotIn("Buy groceries", self.driver.page_source)

    def test_navigate_back_to_login(self):
        # Functionalities 6: Navigate Back to Login
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_invalid_access(self):
        # Functionalities 8: Attempt to access home page without logging in
        self.driver.get('http://localhost:8427/home')
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Session Management
        self.login("user1", "user123")
        self.driver.quit()  # Close the browser
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8427/home')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
