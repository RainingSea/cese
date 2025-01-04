import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

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
        # Test case 1: User Login
        self.login("admin", "admin123")
        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Test case 2: Navigate to Registration Page
        # Assuming there is a 'Register here' link on the login page
        try:
            self.driver.find_element(By.LINK_TEXT, 'Register here').click()
            time.sleep(1)  # Wait for the next page to load
            # Verify that the Registration Page has loaded
            self.assertIn("Register", self.driver.title)
        except:
            self.fail("Registration page navigation not implemented")

    def test_user_registration(self):
        # Test case 3: User Registration
        # Assuming there is a registration page accessible
        try:
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
            self.assertIn("Login", self.driver.title)
        except:
            self.fail("User registration not implemented")

    def test_view_sustainable_living_intro(self):
        # Test case 4: View Sustainable Living Introduction
        self.login("admin", "admin123")
        # Verify that the introduction is displayed on the Dashboard
        self.assertIn("Introduction to Sustainable Living", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Test case 5: View and Submit Sustainable Living Tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Tips').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that tips are displayed
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip = "Use energy-efficient light bulbs."
        self.driver.find_element(By.NAME, 'tip_content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify that the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Test case 6: Read and Submit Articles
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Articles').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        new_article_title = "Green Energy Solutions"
        new_article_content = "Exploring renewable energy sources."
        self.driver.find_element(By.NAME, 'article_title').send_keys(new_article_title)
        self.driver.find_element(By.NAME, 'article_content').send_keys(new_article_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify that the new article is displayed
        self.assertIn(new_article_title, self.driver.page_source)

    def test_participate_in_forum(self):
        # Test case 7: Participate in the Community Forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that forum posts are displayed
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No forum posts found.")

        # Post a new question
        new_post_content = "What are the benefits of solar panels?"
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'post_content').send_keys(new_post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify that the new post is displayed
        self.assertIn(new_post_content, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Test case 8: Navigation to Other Sections
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Articles').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Articles", self.driver.title)

        self.driver.find_element(By.LINK_TEXT, 'View Tips').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Tips", self.driver.title)

        self.driver.find_element(By.LINK_TEXT, 'Community Forum').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Test case 9: Data Storage Verification
        # This test case requires file system access, which is not covered by Selenium.
        # Implementing this would require reading the .txt files directly.
        self.fail("Data storage verification not implemented")

    def test_logout_functionality(self):
        # Test case 10: Logout Functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
