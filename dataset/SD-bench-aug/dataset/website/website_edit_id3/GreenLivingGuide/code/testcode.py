import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/Datasets/SD-bench/codebase/website/GreenLivingGuide/code')
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8132')

    def tearDown(self):
        # Close the web driver session and terminate the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test 1: User Login
        self.login("admin", "adminpass")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Test 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Test 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_view_sustainable_living_introduction(self):
        # Test 4: View Sustainable Living Introduction
        self.login("admin", "adminpass")
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_submit_sustainable_living_tips(self):
        # Test 5: View and Submit Sustainable Living Tips
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0, "No tips found.")
        new_tip = "Use solar panels"
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Test 6: Read and Submit Articles
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")
        new_title = "Green Energy"
        new_content = "The future of sustainable energy."
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)
        self.assertIn(new_title, self.driver.page_source)

    def test_participate_in_community_forum(self):
        # Test 7: Participate in the Community Forum
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No forum posts found.")
        new_post = "How to reduce carbon footprint?"
        self.driver.find_element(By.NAME, 'post').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Post"]').click()
        time.sleep(1)
        self.assertIn(new_post, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Test 8: Navigation to Other Sections
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)
        self.assertIn("Submit Articles", self.driver.title)
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)
        self.assertIn("Submit Tips", self.driver.title)
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)
        self.assertIn("Community Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Test 9: Data Storage Verification
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        new_username = "storage_user"
        new_password = "storage_pass"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        with open('D:/Project/Datasets/SD-bench/codebase/website/GreenLivingGuide/code/users.txt', 'r') as f:
            users = f.read()
            self.assertIn(f"{new_username}|{new_password}", users)

    def test_logout_functionality(self):
        # Test 10: Logout Functionality
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
