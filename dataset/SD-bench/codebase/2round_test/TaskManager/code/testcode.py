import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the app to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8076')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test Case 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Test Case 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "test_user"
        new_password = "test_password"
        new_email = "test_user@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Test Case 3: View Task List
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Test Case 4: Add New Task
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'description').send_keys("Test Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)  # Wait for the task to be added

        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertTrue(any("Test Task" in task.text for task in tasks), "Task not added.")

    def test_remove_task(self):
        # Test Case 5: Remove Task
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the task to be removed

        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertFalse(any("New Task" in task.text for task in tasks), "Task not removed.")

    def test_navigate_back_to_login(self):
        # Test Case 6: Navigate Back to Login
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_task_data_storage(self):
        # Test Case 7: Task Data Storage
        self.fail("Not implemented")

    def test_invalid_actions(self):
        # Test Case 8: Invalid Actions
        self.driver.get('http://localhost:8076/home')
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Test Case 9: Session Management
        self.login("admin", "admin123")
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8076/home')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
