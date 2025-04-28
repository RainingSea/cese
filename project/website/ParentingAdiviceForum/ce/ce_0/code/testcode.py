import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8386/')  # Access the login page

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
        self.assertIn("Home", self.driver.title)  # Expecting to be redirected to Home Page

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.assertIn("Register", self.driver.title)  # Expecting to be on Registration Page

    def test_user_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_home_page_after_login(self):
        # Functionalities 4: View Home Page After Login
        self.login("admin", "admin123")
        self.assertIn("Welcome to the Home Page", self.driver.page_source)  # Check for Home Page content

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Navigate to Forum Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        self.assertIn("Forum", self.driver.title)  # Expecting to be on Forum Page

    def test_create_new_thread(self):
        # Functionalities 6: Create New Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        # Assuming there is a button to create a new thread
        self.driver.find_element(By.LINK_TEXT, 'Create New Thread').click()  # This link/button needs to exist in the forum page
        self.driver.find_element(By.NAME, 'title').send_keys("New Thread Title")
        self.driver.find_element(By.NAME, 'content').send_keys("Content of the new thread.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()  # Assuming a submit button exists

        # Verify that the new thread is displayed on the Forum Page
        self.assertIn("New Thread Title", self.driver.page_source)

    def test_view_specific_thread(self):
        # Functionalities 7: View Specific Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        # Assuming the first thread is clickable
        self.driver.find_element(By.XPATH, '//a[contains(text(), "First Thread")]').click()
        self.assertIn("First Thread", self.driver.title)  # Expecting to be on the specific thread page

    def test_comment_on_thread(self):
        # Functionalities 8: Comment on a Thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        self.driver.find_element(By.XPATH, '//a[contains(text(), "First Thread")]').click()
        self.driver.find_element(By.NAME, 'comment').send_keys("This is a comment.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()  # Assuming a submit button exists

        # Verify that the comment is displayed below the thread
        self.assertIn("This is a comment.", self.driver.page_source)

    def test_post_advice(self):
        # Functionalities 9: Post Advice
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        self.driver.find_element(By.NAME, 'title').send_keys("Advice Title")
        self.driver.find_element(By.NAME, 'content').send_keys("Content of the advice.")
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()  # Assuming a submit button exists

        # Verify that the advice is displayed on the Home Page or Advice Page
        self.assertIn("Advice Title", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
