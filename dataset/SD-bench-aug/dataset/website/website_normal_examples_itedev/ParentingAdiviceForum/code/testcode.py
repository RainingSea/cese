import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver session and terminate the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000')
        self.driver.find_element(By.LINK_TEXT, 'My Account').click()
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Update Account"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test case for user login
        self.login("user1", "p1")
        self.assertIn("Parenting Advice Forum", self.driver.title)

    def test_user_registration(self):
        # Test case for user registration
        self.fail("User registration functionality not implemented")

    def test_navigation_to_home_page(self):
        # Test case for navigation to Home Page
        self.login("user1", "p1")
        self.assertIn("Welcome to the Parenting Advice Forum", self.driver.page_source)

    def test_viewing_discussion_threads(self):
        # Test case for viewing discussion threads
        self.login("user1", "p1")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.assertIn("Forum Threads", self.driver.page_source)

    def test_creating_new_thread(self):
        # Test case for creating a new thread
        self.fail("Creating a new thread functionality not implemented")

    def test_viewing_a_thread(self):
        # Test case for viewing a thread
        self.login("user1", "p1")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.LINK_TEXT, 'Thread Title 1').click()
        self.assertIn("This is the content of thread 1", self.driver.page_source)

    def test_commenting_on_a_thread(self):
        # Test case for commenting on a thread
        self.login("user1", "p1")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.LINK_TEXT, 'Thread Title 1').click()
        self.driver.find_element(By.NAME, 'comment').send_keys("This is a test comment.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        self.assertIn("This is a test comment.", self.driver.page_source)

    def test_posting_advice(self):
        # Test case for posting advice
        self.login("user1", "p1")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        self.driver.find_element(By.NAME, 'title').send_keys("Test Advice Title")
        self.driver.find_element(By.NAME, 'content').send_keys("This is test advice content.")
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()
        self.assertIn("Welcome to the Parenting Advice Forum", self.driver.page_source)

    def test_my_account_management(self):
        # Test case for my account management
        self.login("user1", "p1")
        self.driver.find_element(By.LINK_TEXT, 'My Account').click()
        self.assertIn("My Account", self.driver.page_source)

    def test_contact_us_page(self):
        # Test case for contact us page
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()
        self.driver.find_element(By.NAME, 'name').send_keys("Test User")
        self.driver.find_element(By.NAME, 'email').send_keys("test@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        self.assertIn("Your message has been sent successfully!", self.driver.page_source)

    def test_confirmation_messages(self):
        # Test case for confirmation messages
        self.fail("Confirmation messages functionality not fully implemented")

if __name__ == '__main__':
    unittest.main()
