import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self.driver.get('http://localhost:8118/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('home'))

    def test_1_user_login(self):
        """Functionalities 1: Test valid user login"""
        self.login("admin", "admin123")
        self.assertIn('Welcome', self.driver.page_source)
        self.assertIn('home', self.driver.current_url)

    def test_2_user_registration(self):
        """Functionalities 2: Test user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Generate unique username for testing
        test_username = f"testuser{int(time.time())}"
        test_password = "testpass123"
        test_email = f"{test_username}@example.com"
        
        self.driver.find_element(By.ID, 'username').send_keys(test_username)
        self.driver.find_element(By.ID, 'password').send_keys(test_password)
        self.driver.find_element(By.ID, 'email').send_keys(test_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

    def test_3_view_task_list(self):
        """Functionalities 3: Test viewing task list"""
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(tasks), 0, "No tasks found for admin user")

    def test_4_add_new_task(self):
        """Functionalities 4: Test adding new task"""
        self.login("admin", "admin123")
        
        # Get initial task count
        initial_tasks = len(self.driver.find_elements(By.CLASS_NAME, 'list-group-item'))
        
        # Add new task
        self.driver.find_element(By.ID, 'description').send_keys('New test task')
        self.driver.find_element(By.ID, 'due_date').send_keys('2023-12-31')
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        
        # Wait for page reload
        time.sleep(1)
        
        # Verify task was added
        updated_tasks = len(self.driver.find_elements(By.CLASS_NAME, 'list-group-item'))
        self.assertEqual(updated_tasks, initial_tasks + 1)

    def test_5_remove_task(self):
        """Functionalities 5: Test removing task"""
        self.login("admin", "admin123")
        
        # Get initial task count
        initial_tasks = len(self.driver.find_elements(By.CLASS_NAME, 'list-group-item'))
        if initial_tasks == 0:
            self.skipTest("No tasks available to remove")
        
        # Remove first task
        remove_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Remove"]')
        remove_buttons[0].click()
        
        # Wait for page reload
        time.sleep(1)
        
        # Verify task was removed
        updated_tasks = len(self.driver.find_elements(By.CLASS_NAME, 'list-group-item'))
        self.assertEqual(updated_tasks, initial_tasks - 1)

    def test_6_navigate_back_to_login(self):
        """Functionalities 6: Test logout navigation"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

    def test_7_task_data_storage(self):
        """Functionalities 7: Test task data storage"""
        # First check file content before adding
        with open('tasks.txt', 'r') as f:
            initial_content = f.read()
        
        # Add a new task through UI
        self.login("admin", "admin123")
        self.driver.find_element(By.ID, 'description').send_keys('Storage test task')
        self.driver.find_element(By.ID, 'due_date').send_keys('2023-12-31')
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        time.sleep(1)
        
        # Check file was updated
        with open('tasks.txt', 'r') as f:
            updated_content = f.read()
        self.assertNotEqual(initial_content, updated_content)
        self.assertIn('Storage test task', updated_content)
        
        # Now test removal
        initial_content = updated_content
        remove_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Remove"]')
        remove_buttons[-1].click()  # Remove the last added task
        time.sleep(1)
        
        with open('tasks.txt', 'r') as f:
            updated_content = f.read()
        self.assertNotEqual(initial_content, updated_content)
        self.assertNotIn('Storage test task', updated_content)

    def test_8_invalid_actions(self):
        """Functionalities 8: Test invalid access attempts"""
        # Try to access home page directly without login
        self.driver.get('http://localhost:8118/home')
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

    def test_9_session_management(self):
        """Functionalities 9: Test session management"""
        self.login("admin", "admin123")
        
        # Close and reopen browser
        self.driver.quit()
        self.driver = webdriver.Chrome()
        
        # Try to access home page directly
        self.driver.get('http://localhost:8118/home')
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

if __name__ == '__main__':
    unittest.main()
