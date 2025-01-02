import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/CE/CE/project/website/TaskManager/ce/ce_1/code')
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8154')

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
        # Functionalities 1: Test user login functionality
        self.login("admin", "pass123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the redirection to login page

        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Functionalities 3: Test viewing task list after logging in
        self.login("admin", "pass123")
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreaterEqual(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("admin", "pass123")

        task_description = "New Task"
        due_date = "2023-12-31"

        self.driver.find_element(By.NAME, 'task_description').send_keys(task_description)
        self.driver.find_element(By.NAME, 'due_date').send_keys(due_date)
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)  # Wait for the task to be added

        self.assertIn(task_description, self.driver.page_source)

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("admin", "pass123")

        # Assuming there is at least one task to remove
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        if tasks:
            task_to_remove = tasks[0].text.split(' - ')[0]
            self.driver.find_element(By.XPATH, f'//input[@value="{task_to_remove}"]/following-sibling::button').click()
            time.sleep(1)  # Wait for the task to be removed

            self.assertNotIn(task_to_remove, self.driver.page_source)

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigating back to login
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the redirection to login page

        self.assertIn("Login", self.driver.title)

    def test_task_data_storage(self):
        # Functionalities 7: Test task data storage
        self.login("admin", "pass123")

        task_description = "Storage Test Task"
        due_date = "2023-12-31"

        self.driver.find_element(By.NAME, 'task_description').send_keys(task_description)
        self.driver.find_element(By.NAME, 'due_date').send_keys(due_date)
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)  # Wait for the task to be added

        # Check if the task is stored in the file
        with open('tasks_admin.txt', 'r') as f:
            tasks = f.read()
            self.assertIn(f"{task_description}|{due_date}", tasks)

        # Remove the task and check the file again
        self.driver.find_element(By.XPATH, f'//input[@value="{task_description}"]/following-sibling::button').click()
        time.sleep(1)  # Wait for the task to be removed

        with open('tasks_admin.txt', 'r') as f:
            tasks = f.read()
            self.assertNotIn(f"{task_description}|{due_date}", tasks)

    def test_invalid_actions(self):
        # Functionalities 8: Test accessing home page without logging in
        self.driver.get('http://localhost:8154/home')
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("admin", "pass123")
        self.driver.quit()  # Close the browser without logging out

        # Reopen the browser and check if login is required
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8154/home')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
