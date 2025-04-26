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
        self.driver.get('http://localhost:8255/')  # Use the port defined in main.py

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
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Verify that the home page has loaded

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.get('http://localhost:8255/register')  # Navigate to registration page
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.NAME, 'email').send_keys("new_user@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Functionalities 3: Test viewing task list after logging in
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'add_task').click()

        # Verify that the task has been added
        tasks = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertIn("New Task", [task.text for task in tasks])

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("admin", "admin123")
        tasks_before = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        if tasks_before:
            self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()

            # Verify that the task has been removed
            tasks_after = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
            self.assertNotIn(tasks_before[0].text, [task.text for task in tasks_after])

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigation back to login page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_task_data_storage(self):
        # Functionalities 7: Test task data storage
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("File Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'add_task').click()

        # Check if the task is stored in the file
        with open('tasks_admin.txt', 'r') as file:
            tasks = file.readlines()
            self.assertIn("File Task,2023-12-31\n", tasks)

        # Remove the task for cleanup
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()

    def test_access_home_without_login(self):
        # Functionalities 8: Test access to home page without logging in
        self.driver.get('http://localhost:8255/home')
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("admin", "admin123")
        self.driver.quit()  # Close the browser
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8255/home')
        self.assertIn("Login", self.driver.title)  # Should redirect to login

if __name__ == '__main__':
    unittest.main()
