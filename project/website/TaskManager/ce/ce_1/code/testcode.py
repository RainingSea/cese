import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8195/') 

    def tearDown(self):
        # Close the web driver session and stop the server
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
        self.login("testuser", "testpass")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "newuser"
        new_password = "newpass"
        new_email = "newuser@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Functionalities 3: Test viewing task list after logging in
        self.login("testuser", "testpass")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("testuser", "testpass")
        self.driver.find_element(By.NAME, 'task_description').send_keys("New Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)  # Wait for the task to be added

        self.assertIn("New Task", self.driver.page_source)

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("testuser", "testpass")
        initial_tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        if initial_tasks:
            initial_task_count = len(initial_tasks)
            initial_tasks[0].find_element(By.XPATH, './/button[text()="Remove"]').click()
            time.sleep(1)  # Wait for the task to be removed
            final_tasks = self.driver.find_elements(By.TAG_NAME, 'li')
            self.assertEqual(len(final_tasks), initial_task_count - 1)
        else:
            self.fail("No tasks available to remove.")

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigating back to login
        self.login("testuser", "testpass")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)

    def test_task_data_storage(self):
        # Functionalities 7: Test task data storage
        self.login("testuser", "testpass")
        self.driver.find_element(By.NAME, 'task_description').send_keys("Storage Test Task")
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)  # Wait for the task to be added

        with open('tasks_testuser.txt', 'r') as file:
            tasks = file.read()
            self.assertIn("Storage Test Task", tasks)

        # Remove the task and check the file again
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the task to be removed

        with open('tasks_testuser.txt', 'r') as file:
            tasks = file.read()
            self.assertNotIn("Storage Test Task", tasks)

    def test_invalid_actions(self):
        # Functionalities 8: Test accessing home page without logging in
        self.driver.get('http://localhost:8195/home')
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("testuser", "testpass")
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8195/home')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
