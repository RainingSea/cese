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
        self.driver.get('http://localhost:8138')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
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

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_navigation_to_home_page(self):
        # Test case for navigation to Home Page
        self.login("admin", "adminpass")
        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

    def test_viewing_discussion_threads(self):
        # Test case for viewing discussion threads
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        threads = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(threads), 0, "No discussion threads found.")

    def test_creating_new_thread(self):
        # Test case for creating a new thread
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        thread_title = "New Thread Title"
        thread_content = "This is the content of the new thread."

        self.driver.find_element(By.NAME, 'title').send_keys(thread_title)
        self.driver.find_element(By.NAME, 'content').send_keys(thread_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Thread"]').click()
        time.sleep(1)  # Wait for the thread to be created

        self.assertIn(thread_title, self.driver.page_source)

    def test_viewing_thread(self):
        # Test case for viewing a thread
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        self.driver.find_element(By.LINK_TEXT, 'New Thread Title').click()
        time.sleep(1)  # Wait for the thread page to load

        self.assertIn("New Thread Title", self.driver.page_source)

    def test_commenting_on_thread(self):
        # Test case for commenting on a thread
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the forum page to load

        self.driver.find_element(By.LINK_TEXT, 'New Thread Title').click()
        time.sleep(1)  # Wait for the thread page to load

        comment_content = "This is a new comment."
        self.driver.find_element(By.NAME, 'content').send_keys(comment_content)
        self.driver.find_element(By.XPATH, '//button[text()="Comment"]').click()
        time.sleep(1)  # Wait for the comment to be added

        self.assertIn(comment_content, self.driver.page_source)

    def test_posting_advice(self):
        # Test case for posting advice
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        time.sleep(1)  # Wait for the post advice page to load

        advice_title = "New Advice Title"
        advice_content = "This is the content of the new advice."

        self.driver.find_element(By.NAME, 'title').send_keys(advice_title)
        self.driver.find_element(By.NAME, 'content').send_keys(advice_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()
        time.sleep(1)  # Wait for the advice to be posted

        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

    def test_my_account_management(self):
        # Test case for my account management
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'My Account').click()
        time.sleep(1)  # Wait for the my account page to load

        self.assertIn("My Account", self.driver.page_source)

    def test_contact_us_page(self):
        # Test case for contact us page
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Contact Us').click()
        time.sleep(1)  # Wait for the contact us page to load

        self.driver.find_element(By.NAME, 'name').send_keys("John Doe")
        self.driver.find_element(By.NAME, 'email').send_keys("john.doe@example.com")
        self.driver.find_element(By.NAME, 'message').send_keys("This is a test message.")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        time.sleep(1)  # Wait for the message to be sent

        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

    def test_confirmation_messages(self):
        # Test case for confirmation messages
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        time.sleep(1)  # Wait for the post advice page to load

        advice_title = "Confirmation Advice Title"
        advice_content = "This is the content of the confirmation advice."

        self.driver.find_element(By.NAME, 'title').send_keys(advice_title)
        self.driver.find_element(By.NAME, 'content').send_keys(advice_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()
        time.sleep(1)  # Wait for the advice to be posted

        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
