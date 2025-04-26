import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestGreenLivingGuideApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8172/') 

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
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.get('http://localhost:8172/')  # Go back to login page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.get('http://localhost:8172/')  # Go back to login page
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

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: Test viewing sustainable living introduction after logging in
        self.login("admin", "admin123")
        # Assuming there's a link to the introduction page
        self.driver.find_element(By.LINK_TEXT, 'Introduction').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Introduction to Sustainable Living", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        
        # View existing tips
        tips = self.driver.find_elements(By.CLASS_NAME, 'tip-item')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        self.driver.find_element(By.LINK_TEXT, 'Submit Tip').click()
        time.sleep(1)  # Wait for the next page to load

        new_tip = "Always carry a reusable water bottle."
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")

        # View existing articles
        articles = self.driver.find_elements(By.CLASS_NAME, 'article-item')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        self.driver.find_element(By.LINK_TEXT, 'Submit Article').click()
        time.sleep(1)  # Wait for the next page to load

        new_article = "The Benefits of Urban Gardening"
        self.driver.find_element(By.NAME, 'article').send_keys(new_article)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the article to be submitted

        # Verify the new article is displayed
        self.assertIn(new_article, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test accessing and posting in the community forum
        self.login("admin", "admin123")

        # Access the forum
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the forum to load
        self.assertIn("Community Forum", self.driver.page_source)

        # Post a new question
        self.driver.find_element(By.LINK_TEXT, 'Post a Question').click()
        time.sleep(1)  # Wait for the next page to load

        new_question = "What are some eco-friendly home improvements?"
        self.driver.find_element(By.NAME, 'question').send_keys(new_question)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the question to be posted

        # Verify the new question is displayed
        self.assertIn(new_question, self.driver.page_source)

    def test_logout_functionality(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)

    def test_data_storage_verification(self):
        # Functionalities 9: Test data storage verification
        self.login("admin", "admin123")

        # Check if the user details are saved correctly in users.txt
        with open('users.txt', 'r') as file:
            users = file.readlines()
            self.assertIn("new_user|new_password\n", users)

        # Check if the new tip is saved correctly in tips.txt
        with open('tips.txt', 'r') as file:
            tips = file.readlines()
            self.assertIn("Always carry a reusable water bottle.\n", tips)

        # Check if the new article is saved correctly in articles.txt
        with open('articles.txt', 'r') as file:
            articles = file.readlines()
            self.assertIn("The Benefits of Urban Gardening\n", articles)

if __name__ == '__main__':
    unittest.main()
