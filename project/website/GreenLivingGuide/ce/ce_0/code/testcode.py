import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/CE/CE/project/website/GreenLivingGuide/ce/ce_0/code')
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8167')

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

    def test_view_sustainable_living_introduction(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("admin", "pass123")

        # Verify that the introduction is displayed
        self.assertIn("Welcome", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that tips are displayed
        self.assertIn("Reduce, Reuse, Recycle", self.driver.page_source)

        # Submit a new tip
        self.driver.find_element(By.NAME, 'content').send_keys("Use solar panels")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be saved

        # Verify the new tip is displayed
        self.assertIn("Use solar panels", self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that articles are displayed
        self.assertIn("The Benefits of Sustainable Living", self.driver.page_source)

        # Submit a new article
        self.driver.find_element(By.NAME, 'title').send_keys("New Article")
        self.driver.find_element(By.NAME, 'content').send_keys("Content of the new article")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be saved

        # Verify the new article is displayed
        self.assertIn("New Article", self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participating in the community forum
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that forum posts are displayed
        self.assertIn("What are some easy ways to live sustainably?", self.driver.page_source)

        # Post a new question
        self.driver.find_element(By.NAME, 'content').send_keys("How to reduce carbon footprint?")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Post"]').click()
        time.sleep(1)  # Wait for the post to be saved

        # Verify the new post is displayed
        self.assertIn("How to reduce carbon footprint?", self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify navigation to Articles section
        self.assertIn("Articles", self.driver.page_source)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        new_username = "storage_test_user"
        new_password = "storage_test_pass"

        # Register a new user
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the registration to complete

        # Verify user details in users.txt
        with open('D:/Project/CE/CE/project/website/GreenLivingGuide/ce/ce_0/code/users.txt', 'r') as f:
            users = f.read()
            self.assertIn(f"{new_username}|{new_password}", users)

    def test_logout(self):
        # Functionalities 10: Test logout functionality
        self.login("admin", "pass123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
