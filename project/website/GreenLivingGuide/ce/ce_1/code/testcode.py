import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestGreenLivingGuideApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8169')

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

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "pass123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.page_source)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("admin", "pass123")

        # Verify that the introduction is displayed (assuming it's on the dashboard)
        self.assertIn("Welcome", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)

        # Verify existing tips are displayed
        self.assertIn("Tips List", self.driver.page_source)

        # Submit a new tip
        new_tip = "Use solar panels for energy"
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)

        # Verify the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)

        # Verify existing articles are displayed
        self.assertIn("Articles List", self.driver.page_source)

        # Submit a new article
        new_article_title = "New Sustainable Practice"
        new_article_content = "Details about new sustainable practice."
        self.driver.find_element(By.NAME, 'title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)

        # Verify the new article is displayed
        self.assertIn(new_article_title, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)

        # Verify the forum is loaded
        self.assertIn("Community Forum", self.driver.page_source)

        # Post a new question
        new_post = "What are the best ways to conserve water?"
        self.driver.find_element(By.NAME, 'content').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Post"]').click()
        time.sleep(1)

        # Verify the new post is displayed
        self.assertIn(new_post, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "pass123")

        # Navigate to Tips
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)
        self.assertIn("Tips List", self.driver.page_source)

        # Navigate to Articles
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)
        self.assertIn("Articles List", self.driver.page_source)

        # Navigate to Forum
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)
        self.assertIn("Community Forum", self.driver.page_source)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        # This test would require checking the file system, which is not feasible with Selenium directly.
        # Instead, we can verify the presence of data on the UI as an indirect check.
        self.fail("Data storage verification not implemented in Selenium tests.")

    def test_logout(self):
        # Functionalities 10: Test logout functionality
        self.login("admin", "pass123")

        # Click the Logout button (assuming there's a logout link or button)
        # self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        # time.sleep(1)

        # Verify that the user is redirected to the Login Page
        # self.assertIn("Login", self.driver.page_source)
        self.fail("Logout functionality not implemented in the application.")

if __name__ == '__main__':
    unittest.main()
