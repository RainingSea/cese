import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8215/')  # Access the login page

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
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Expectation: Redirected to Home Page

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)  # Expectation: Redirected to Registration Page

    def test_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)  # Expectation: Redirected to Login Page

    def test_view_home_page_after_login(self):
        # Functionalities 4: View Home Page After Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Expectation: Home Page loaded

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Navigate to Forum Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.assertIn("Forum", self.driver.title)  # Expectation: Redirected to Forum Page

    def test_create_new_thread(self):
        # Functionalities 6: Create New Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.NAME, 'title').send_keys("New Thread Title")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of the new thread.")
        self.driver.find_element(By.XPATH, '//button[text()="Create Thread"]').click()
        self.assertIn("Forum", self.driver.title)  # Expectation: Redirected to Forum Page

    def test_view_specific_thread(self):
        # Functionalities 7: View Specific Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.XPATH, '//li/a').click()  # Click on the first thread
        self.assertIn("View Thread", self.driver.title)  # Expectation: Redirected to View Thread Page

    def test_comment_on_thread(self):
        # Functionalities 8: Comment on a Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.XPATH, '//li/a').click()  # Click on the first thread
        self.driver.find_element(By.NAME, 'comment').send_keys("This is a comment.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Comment"]').click()
        self.assertIn("This is a comment.", self.driver.page_source)  # Expectation: Comment is displayed

    def test_post_advice(self):
        # Functionalities 9: Post Advice
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        self.driver.find_element(By.NAME, 'title').send_keys("Advice Title")
        self.driver.find_element(By.NAME, 'content').send_keys("This is some advice content.")
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()
        self.assertIn("Forum", self.driver.title)  # Expectation: Redirected to Forum Page

if __name__ == '__main__':
    unittest.main()
