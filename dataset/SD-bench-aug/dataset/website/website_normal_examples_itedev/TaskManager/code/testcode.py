import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/Datasets/SD-bench/codebase/website/TaskManager/code')
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver session and terminate the web application
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
        self.assertIn("Task Manager", self.driver.page_source)

    def test_user_registration(self):
        # Test Case 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        new_username = "testuser"
        new_password = "testpass"
        new_email = "testuser@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()
        time.sleep(1)

        self.assertIn("Login", self.driver.page_source)

    def test_view_task_list(self):
        # Test Case 3: View Task List
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreaterEqual(len(tasks), 0)

    def test_add_new_task(self):
        # Test Case 4: Add New Task
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)

        self.assertIn("New Task", self.driver.page_source)

    def test_remove_task(self):
        # Test Case 5: Remove Task
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("Task to Remove")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)

        self.driver.find_element(By.XPATH, '//button[text()="Remove Task"]').click()
        time.sleep(1)

        self.assertNotIn("Task to Remove", self.driver.page_source)

    def test_navigate_back_to_login(self):
        # Test Case 6: Navigate Back to Login
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Back to Login').click()
        time.sleep(1)

        self.assertIn("Login", self.driver.page_source)

    def test_task_data_storage(self):
        # Test Case 7: Task Data Storage
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("Persistent Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)

        with open('tasks_admin.txt', 'r') as file:
            tasks = file.read()
            self.assertIn("Persistent Task", tasks)

        self.driver.find_element(By.XPATH, '//button[text()="Remove Task"]').click()
        time.sleep(1)

        with open('tasks_admin.txt', 'r') as file:
            tasks = file.read()
            self.assertNotIn("Persistent Task", tasks)

    def test_invalid_actions(self):
        # Test Case 8: Invalid Actions
        self.driver.get('http://localhost:5000/home')
        time.sleep(1)

        self.assertIn("Login", self.driver.page_source)

    def test_session_management(self):
        # Test Case 9: Session Management
        self.login("admin", "admin123")
        self.driver.quit()

        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/home')
        time.sleep(1)

        self.assertIn("Login", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
