import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/CE/CE/project/website/GreenLivingGuide/ce/ce_2/code')
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8952/')

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)

    def test_view_sustainable_living_introduction(self):
        # Functionalities 4: Test viewing sustainable living introduction
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        self.assertIn("Sustainable Living Tips", self.driver.title)

        # Submit a new tip
        new_tip = "Use public transport"
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        self.assertIn("Articles", self.driver.title)

        # Submit a new article
        new_title = "Green Energy"
        new_content = "The benefits of using green energy."
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        self.assertIn(new_title, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test participation in the community forum
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.assertIn("Community Forum", self.driver.title)

        # Post a new question
        new_post = "How do you reduce waste?"
        self.driver.find_element(By.NAME, 'content').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Post"]').click()
        self.assertIn(new_post, self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        self.assertIn("Sustainable Living Tips", self.driver.title)

        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        self.assertIn("Articles", self.driver.title)

        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.assertIn("Community Forum", self.driver.title)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify user details in users.txt
        with open('D:/Project/CE/CE/project/website/GreenLivingGuide/ce/ce_2/code/users.txt', 'r') as f:
            users = f.read()
        self.assertIn(f"{new_username}|{new_password}", users)

        # Verify tip in tips.txt
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        new_tip = "Use less plastic"
        self.driver.find_element(By.NAME, 'content').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()

        with open('D:/Project/CE/CE/project/website/GreenLivingGuide/ce/ce_2/code/tips.txt', 'r') as f:
            tips = f.read()
        self.assertIn(new_tip, tips)

        # Verify article in articles.txt
        self.driver.find_element(By.LINK_TEXT, 'Articles').click()
        new_title = "Eco-Friendly Homes"
        new_content = "Building homes with sustainable materials."
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()

        with open('D:/Project/CE/CE/project/website/GreenLivingGuide/ce/ce_2/code/articles.txt', 'r') as f:
            articles = f.read()
        self.assertIn(f"{new_title}|{new_content}", articles)

    def test_logout(self):
        # Functionalities 10: Test logout functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
