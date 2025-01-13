import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8495/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and terminate the application
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
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Functionalities 3: Test viewing task list after logging in
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("New Task|2023-12-31", [task.text for task in tasks])

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("admin", "admin123")
        initial_tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        if initial_tasks:
            initial_task_count = len(initial_tasks)
            initial_tasks[0].find_element(By.NAME, 'remove_task').click()
            time.sleep(1)  # Wait for the task to be removed

            tasks_after_removal = self.driver.find_elements(By.TAG_NAME, 'li')
            self.assertEqual(len(tasks_after_removal), initial_task_count - 1)
        else:
            self.fail("No tasks available to remove.")

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigating back to login
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_task_data_storage(self):
        # Functionalities 7: Test task data storage
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'task_description').send_keys("Storage Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'add_task').click()
        time.sleep(1)  # Wait for the task to be added

        tasks_file = 'tasks_admin.txt'
        with open(tasks_file, 'r') as f:
            tasks = f.read()
            self.assertIn("Storage Task|2023-12-31", tasks)

        # Remove the task and check the file again
        tasks_list = self.driver.find_elements(By.TAG_NAME, 'li')
        for task in tasks_list:
            if "Storage Task|2023-12-31" in task.text:
                task.find_element(By.NAME, 'remove_task').click()
                break
        time.sleep(1)  # Wait for the task to be removed

        with open(tasks_file, 'r') as f:
            tasks = f.read()
            self.assertNotIn("Storage Task|2023-12-31", tasks)

    def test_invalid_actions(self):
        # Functionalities 8: Test accessing home page without logging in
        self.driver.get('http://localhost:8495/home')
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("admin", "admin123")
        self.driver.quit()  # Close the browser without logging out

        # Reopen the browser and check session validity
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8495/home')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
