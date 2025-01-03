import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/my_account')
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")  # Use valid credentials
        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

    def test_view_forum_threads(self):
        # Test viewing discussion threads
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Forum Threads", self.driver.page_source)

    def test_create_new_thread(self):
        # Test creating a new thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        time.sleep(1)
        
        self.driver.find_element(By.NAME, 'title').send_keys("New Parenting Tips")
        self.driver.find_element(By.NAME, 'content').send_keys("Here are some new tips for parents.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Advice"]').click()
        time.sleep(1)

        self.assertIn("New Parenting Tips", self.driver.page_source)

    def test_view_thread(self):
        # Test viewing a thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Parenting Tips').click()  # Assuming this thread exists
        time.sleep(1)

        self.assertIn("Parenting Tips", self.driver.page_source)

    def test_comment_on_thread(self):
        # Test commenting on a thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Parenting Tips').click()
        time.sleep(1)

        self.driver.find_element(By.NAME, 'comment').send_keys("Great advice!")
        self.driver.find_element(By.XPATH, '//button[text()="Post Comment"]').click()
        time.sleep(1)

        self.assertIn("Great advice!", self.driver.page_source)

    def test_post_advice(self):
        # Test posting advice
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        time.sleep(1)

        self.driver.find_element(By.NAME, 'title').send_keys("New Advice Title")
        self.driver.find_element(By.NAME, 'content').send_keys("Content for new advice.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Advice"]').click()
        time.sleep(1)

        self.assertIn("New Advice Title", self.driver.page_source)

    def test_contact_us(self):
        # Test submitting a contact inquiry
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()
        time.sleep(1)

        self.driver.find_element(By.NAME, 'name').send_keys("John Doe")
        self.driver.find_element(By.NAME, 'email').send_keys("john@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send Message"]').click()
        time.sleep(1)

        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
