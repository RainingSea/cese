import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\codebase\\website\\ParentingAdiviceForum\\code')
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8546/')

    def tearDown(self):
        # Close the browser and stop the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(2)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.page_source)

    def test_navigate_to_registration_page(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(2)
        self.assertIn("Register", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(2)
        self.driver.find_element(By.NAME, 'username').send_keys("testuser")
        self.driver.find_element(By.NAME, 'password').send_keys("testpassword")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(2)
        self.assertIn("Login", self.driver.page_source)

    def test_view_home_page_after_login(self):
        # Functionalities 4: View Home Page After Login
        self.login("admin", "admin123")
        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Navigate to Forum Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(2)
        self.assertIn("Forum Threads", self.driver.page_source)

    def test_create_new_thread(self):
        # Functionalities 6: Create New Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, 'Create New Thread').click()
        time.sleep(2)
        self.driver.find_element(By.NAME, 'title').send_keys("Test Thread")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a test thread.")
        self.driver.find_element(By.XPATH, '//button[text()="Create Thread"]').click()
        time.sleep(2)
        self.assertIn("Test Thread", self.driver.page_source)

    def test_view_specific_thread(self):
        # Functionalities 7: View Specific Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, 'First Thread').click()
        time.sleep(2)
        self.assertIn("This is the content of the first thread.", self.driver.page_source)

    def test_comment_on_thread(self):
        # Functionalities 8: Comment on a Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, 'First Thread').click()
        time.sleep(2)
        self.driver.find_element(By.NAME, 'comment').send_keys("This is a test comment.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(2)
        self.assertIn("This is a test comment.", self.driver.page_source)

    def test_post_advice(self):
        # Functionalities 9: Post Advice
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        time.sleep(2)
        self.driver.find_element(By.NAME, 'title').send_keys("Test Advice")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a test advice.")
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()
        time.sleep(2)
        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
