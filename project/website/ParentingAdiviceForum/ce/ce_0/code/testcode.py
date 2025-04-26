import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8214/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        username = "new_user"
        password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)

    def test_view_home_page_after_login(self):
        # Functionalities 4: View Home Page After Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)
        self.assertIn("Forum", self.driver.page_source)
        self.assertIn("Post Advice", self.driver.page_source)
        self.assertIn("My Account", self.driver.page_source)
        self.assertIn("Contact Us", self.driver.page_source)

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Navigate to Forum Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.assertIn("Forum", self.driver.title)

    def test_create_new_thread(self):
        # Functionalities 6: Create New Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Thread').click()
        title = "New Thread Title"
        content = "This is the content of the new thread."
        self.driver.find_element(By.NAME, 'title').send_keys(title)
        self.driver.find_element(By.NAME, 'content').send_keys(content)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        self.assertIn(title, self.driver.page_source)

    def test_view_specific_thread(self):
        # Functionalities 7: View Specific Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.LINK_TEXT, 'First Thread').click()
        self.assertIn("First Thread", self.driver.title)

    def test_comment_on_thread(self):
        # Functionalities 8: Comment on a Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.LINK_TEXT, 'First Thread').click()
        comment = "This is a comment."
        self.driver.find_element(By.NAME, 'comment').send_keys(comment)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        self.assertIn(comment, self.driver.page_source)

    def test_post_advice(self):
        # Functionalities 9: Post Advice
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        title = "Advice Title"
        content = "This is some advice content."
        self.driver.find_element(By.NAME, 'title').send_keys(title)
        self.driver.find_element(By.NAME, 'content').send_keys(content)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        self.assertIn(title, self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
