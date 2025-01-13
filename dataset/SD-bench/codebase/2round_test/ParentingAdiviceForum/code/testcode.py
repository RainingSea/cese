import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8073')

    def tearDown(self):
        # Close the web driver session and terminate the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test case for user login
        self.login("admin", "adminpass")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Test case for user registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "unique_user"
        new_password = "strong_password"

        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_navigation_to_home_page(self):
        # Test case for navigation to home page
        self.login("admin", "adminpass")
        self.assertIn("Welcome to the Forum", self.driver.page_source)

    def test_viewing_discussion_threads(self):
        # Test case for viewing discussion threads
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        threads = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(threads), 0, "No discussion threads found.")

    def test_creating_a_new_thread(self):
        # Test case for creating a new thread
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        time.sleep(1)  # Wait for the post advice page to load

        thread_title = "New Thread Title"
        thread_content = "This is the content of the new thread."

        self.driver.find_element(By.ID, 'title').send_keys(thread_title)
        self.driver.find_element(By.ID, 'content').send_keys(thread_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the forum page to load

        self.assertIn(thread_title, self.driver.page_source)

    def test_viewing_a_thread(self):
        # Test case for viewing a thread
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Go to Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        self.driver.find_element(By.LINK_TEXT, 'First Thread').click()
        time.sleep(1)  # Wait for the thread page to load

        self.assertIn("First Thread", self.driver.page_source)
        self.assertIn("This is the content of the first thread.", self.driver.page_source)

    def test_commenting_on_a_thread(self):
        # Test case for commenting on a thread
        self.fail("Not implemented")

    def test_posting_advice(self):
        # Test case for posting advice
        self.fail("Not implemented")

    def test_my_account_management(self):
        # Test case for my account management
        self.fail("Not implemented")

    def test_contact_us_page(self):
        # Test case for contact us page
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()
        time.sleep(1)  # Wait for the contact us page to load

        self.driver.find_element(By.ID, 'name').send_keys("Test User")
        self.driver.find_element(By.ID, 'email').send_keys("test@example.com")
        self.driver.find_element(By.ID, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn("Welcome to the Forum", self.driver.page_source)

    def test_confirmation_messages(self):
        # Test case for confirmation messages
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
