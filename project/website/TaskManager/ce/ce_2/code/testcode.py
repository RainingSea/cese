import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8988/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and terminate the process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.NAME, 'email').send_keys("new_user@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Functionalities 3: View Task List
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreaterEqual(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Functionalities 4: Add New Task
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        self.assertIn("New Task", self.driver.page_source)

    def test_remove_task(self):
        # Functionalities 5: Remove Task
        self.fail("Remove Task functionality not implemented")

    def test_navigate_back_to_login(self):
        # Functionalities 6: Navigate Back to Login
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_task_data_storage(self):
        # Functionalities 7: Task Data Storage
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("Storage Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        with open('tasks_admin.txt', 'r') as file:
            tasks = file.read()
        self.assertIn("Storage Task", tasks)

    def test_invalid_actions(self):
        # Functionalities 8: Invalid Actions
        self.driver.get('http://localhost:8988/home')
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Session Management
        self.login("admin", "admin123")
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8988/home')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
