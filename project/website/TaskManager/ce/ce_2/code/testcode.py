import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import subprocess

class TestTaskManagerApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8119/login')
        self.username = "admin"
        self.password = "admin123"
        self.new_user = "test_user"
        self.new_pass = "test_pass"
        self.new_email = "test@example.com"

    def tearDown(self):
        self.driver.quit()
        # Clean up test data if any
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                lines = f.readlines()
            with open('users.txt', 'w') as f:
                for line in lines:
                    if not line.startswith(f"{self.new_user}:"):
                        f.write(line)
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as f:
                lines = f.readlines()
            with open('tasks.txt', 'w') as f:
                for line in lines:
                    if not line.startswith(f"{self.new_user}:"):
                        f.write(line)

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)

    def test_1_user_login(self):
        """Functionalities 1: Test valid user login"""
        self.login(self.username, self.password)
        self.assertIn("Welcome", self.driver.page_source)
        self.assertIn(self.username, self.driver.page_source)

    def test_2_user_registration(self):
        """Functionalities 2: Test user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        
        self.driver.find_element(By.NAME, 'username').send_keys(self.new_user)
        self.driver.find_element(By.NAME, 'password').send_keys(self.new_pass)
        self.driver.find_element(By.NAME, 'email').send_keys(self.new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        self.assertIn("Login", self.driver.title)
        
        # Verify registration was successful by trying to login
        self.login(self.new_user, self.new_pass)
        self.assertIn("Welcome", self.driver.page_source)
        self.assertIn(self.new_user, self.driver.page_source)

    def test_3_view_task_list(self):
        """Functionalities 3: Test viewing task list"""
        self.login(self.username, self.password)
        tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tasks), 0, "No tasks found for the user")

    def test_4_add_new_task(self):
        """Functionalities 4: Test adding new task"""
        self.login(self.username, self.password)
        
        initial_task_count = len(self.driver.find_elements(By.TAG_NAME, 'li'))
        
        description = "Test task description"
        due_date = "2023-12-31"
        
        self.driver.find_element(By.NAME, 'description').send_keys(description)
        self.driver.find_element(By.NAME, 'due_date').send_keys(due_date)
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)
        
        new_task_count = len(self.driver.find_elements(By.TAG_NAME, 'li'))
        self.assertEqual(new_task_count, initial_task_count + 1)
        self.assertIn(description, self.driver.page_source)
        self.assertIn(due_date, self.driver.page_source)

    def test_5_remove_task(self):
        """Functionalities 5: Test removing task"""
        self.login(self.username, self.password)
        
        initial_tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        if len(initial_tasks) == 0:
            self.skipTest("No tasks available to test removal")
        
        # Get the first task's remove button and click it
        remove_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Remove"]')
        remove_buttons[0].click()
        time.sleep(1)
        
        new_tasks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(new_tasks), len(initial_tasks) - 1)

    def test_6_navigate_back_to_login(self):
        """Functionalities 6: Test logout functionality"""
        self.login(self.username, self.password)
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_7_task_data_storage(self):
        """Functionalities 7: Test task data storage in file"""
        self.login(self.username, self.password)
        
        # Check initial tasks in file
        initial_file_content = ""
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as f:
                initial_file_content = f.read()
        
        # Add a new task
        description = "File storage test task"
        due_date = "2023-12-31"
        
        self.driver.find_element(By.NAME, 'description').send_keys(description)
        self.driver.find_element(By.NAME, 'due_date').send_keys(due_date)
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)
        
        # Check file was updated
        updated_file_content = ""
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as f:
                updated_file_content = f.read()
        
        self.assertNotEqual(initial_file_content, updated_file_content)
        self.assertIn(description, updated_file_content)
        self.assertIn(due_date, updated_file_content)
        
        # Now remove the task
        remove_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Remove"]')
        remove_buttons[-1].click()  # Remove the last added task
        time.sleep(1)
        
        # Check file was updated again
        final_file_content = ""
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as f:
                final_file_content = f.read()
        
        self.assertNotIn(description, final_file_content)

    def test_8_invalid_actions(self):
        """Functionalities 8: Test accessing home without login"""
        self.driver.get('http://localhost:8119/home')
        self.assertIn("Login", self.driver.title)
        self.assertNotIn("Welcome", self.driver.page_source)

    def test_9_session_management(self):
        """Functionalities 9: Test session management"""
        self.login(self.username, self.password)
        self.assertIn("Welcome", self.driver.page_source)
        
        # Close and reopen browser
        self.driver.quit()
        self.driver = webdriver.Chrome()
        
        # Try to access home directly
        self.driver.get('http://localhost:8119/home')
        self.assertIn("Login", self.driver.title)
        self.assertNotIn("Welcome", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
