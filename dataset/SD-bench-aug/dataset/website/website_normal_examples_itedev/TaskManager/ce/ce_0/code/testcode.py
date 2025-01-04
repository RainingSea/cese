import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/CE/CE/project/website/TaskManager_20241226203210/ce/ce_0/code')
        time.sleep(5)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")  # Assuming these credentials exist
        self.assertIn("Task Manager", self.driver.title)

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.get('http://localhost:5000/register')
        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Test viewing task list after logging in
        self.login("admin", "admin123")  # Assuming these credentials exist
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Test adding a new task
        self.login("admin", "admin123")  # Assuming these credentials exist
        self.driver.find_element(By.NAME, 'task_description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        # Verify that the new task appears in the task list
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("New Task", [task.text for task in tasks])

    def test_remove_task(self):
        # Test removing a task
        self.login("admin", "admin123")  # Assuming these credentials exist
        self.driver.find_element(By.NAME, 'task_description').send_keys("Task to Remove")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        # Now remove the task
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        if tasks:
            self.driver.find_element(By.XPATH, '//button[text()="Remove Task"]').click()
            time.sleep(1)  # Wait for the task to be removed
            tasks = self.driver.find_elements(By.TAG_NAME, 'li')
            self.assertNotIn("Task to Remove", [task.text for task in tasks])

    def test_navigate_back_to_login(self):
        # Test navigation back to login page
        self.login("admin", "admin123")  # Assuming these credentials exist
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)

    def test_invalid_access(self):
        # Test access to home page without logging in
        self.driver.get('http://localhost:5000/home')
        time.sleep(1)  # Wait for the redirect
        self.assertIn("Login", self.driver.title)

    def test_task_data_storage(self):
        # Test task data storage in the local text file
        self.login("admin", "admin123")  # Assuming these credentials exist
        self.driver.find_element(By.NAME, 'task_description').send_keys("Persistent Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        # Check the local text file for the task
        with open('tasks_admin.txt', 'r') as file:  # Assuming 'admin' is the username
            tasks = file.readlines()
            self.assertIn("Persistent Task|2023-12-31\n", tasks)

        # Now remove the task
        self.driver.find_element(By.XPATH, '//button[text()="Remove Task"]').click()
        time.sleep(1)  # Wait for the task to be removed

        # Check the local text file to ensure the task is removed
        with open('tasks_admin.txt', 'r') as file:
            tasks = file.readlines()
            self.assertNotIn("Persistent Task|2023-12-31\n", tasks)

if __name__ == '__main__':
    unittest.main()
