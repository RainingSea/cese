import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
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
        self.driver.get('http://localhost:8117/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('/'))

    def test_functionality_1_user_login(self):
        """Test valid user login"""
        self.login("admin", "admin123")
        self.assertIn("Welcome", self.driver.page_source)
        self.assertIn("admin", self.driver.page_source)

    def test_functionality_2_user_registration(self):
        """Test user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.url_contains('/register'))
        
        username = "newuser_" + str(int(time.time()))
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys("newpass123")
        self.driver.find_element(By.NAME, 'email').send_keys(f"{username}@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.url_contains('/login'))
        self.assertIn("Login", self.driver.title)

    def test_functionality_3_view_task_list(self):
        """Test viewing task list after login"""
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertGreater(len(tasks), 0, "No tasks found for admin user")

    def test_functionality_4_add_new_task(self):
        """Test adding a new task"""
        self.login("admin", "admin123")
        
        description = "Test task " + str(int(time.time()))
        due_date = "2023-12-31"
        
        self.driver.find_element(By.NAME, 'description').send_keys(description)
        self.driver.find_element(By.NAME, 'due_date').send_keys(due_date)
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        
        self.wait.until(EC.url_contains('/'))
        self.assertIn(description, self.driver.page_source)

    def test_functionality_5_remove_task(self):
        """Test removing a task"""
        self.login("admin", "admin123")
        
        # First add a task to remove
        description = "Task to remove " + str(int(time.time()))
        self.driver.find_element(By.NAME, 'description').send_keys(description)
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        self.wait.until(EC.url_contains('/'))
        
        # Find and click the remove link for the new task
        tasks = self.driver.find_elements(By.XPATH, '//ul/li')
        for task in tasks:
            if description in task.text:
                task.find_element(By.LINK_TEXT, 'Remove').click()
                break
        
        self.wait.until(EC.url_contains('/'))
        self.assertNotIn(description, self.driver.page_source)

    def test_functionality_6_navigate_back_to_login(self):
        """Test logout functionality"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.url_contains('/login'))
        self.assertIn("Login", self.driver.title)

    def test_functionality_7_task_data_storage(self):
        """Test task data persistence in file"""
        # First check initial state
        initial_tasks = []
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as f:
                initial_tasks = f.readlines()
        
        # Add a new task through UI
        self.login("admin", "admin123")
        description = "Storage test " + str(int(time.time()))
        self.driver.find_element(By.NAME, 'description').send_keys(description)
        self.driver.find_element(By.NAME, 'due_date').send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()
        self.wait.until(EC.url_contains('/'))
        
        # Check file was updated
        found = False
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as f:
                for line in f:
                    try:
                        task = json.loads(line)
                        if task['description'] == description:
                            found = True
                            break
                    except json.JSONDecodeError:
                        continue
        self.assertTrue(found, "New task not found in storage file")

    def test_functionality_8_invalid_actions(self):
        """Test accessing protected pages without login"""
        self.driver.get('http://localhost:8117/')
        self.wait.until(EC.url_contains('/login'))
        self.assertIn("Login", self.driver.title)

    def test_functionality_9_session_management(self):
        """Test session expiration"""
        self.login("admin", "admin123")
        # Close and reopen browser
        self.driver.quit()
        
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8117/')
        self.wait.until(EC.url_contains('/login'))
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
