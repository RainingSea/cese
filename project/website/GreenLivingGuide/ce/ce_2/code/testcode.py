import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestGreenLivingGuideApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the correct port if needed

    def tearDown(self):
        # Close the web driver session and the Flask application
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
        self.assertIn("Home", self.driver.title)  # Check if redirected to home page

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
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
        self.assertIn("Login", self.driver.title)

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: Test viewing sustainable living introduction after logging in
        self.login("admin", "admin123")
        self.assertIn("Welcome to GreenLivingGuide", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        
        # Verify existing tips are displayed
        tips = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming tips are in <li> elements
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip = "Plant more trees"
        self.driver.find_element(By.NAME, 'new_tip').send_keys(new_tip)  # Assuming there's an input for new tips
        self.driver.find_element(By.XPATH, '//button[text()="Submit Tip"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify the new tip is displayed
        self.assertIn(new_tip, self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")

        # Verify existing articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming articles are in <li> elements
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        new_article = "The Benefits of Solar Energy"
        self.driver.find_element(By.NAME, 'new_article').send_keys(new_article)  # Assuming there's an input for new articles
        self.driver.find_element(By.XPATH, '//button[text()="Submit Article"]').click()
        time.sleep(1)  # Wait for the article to be submitted

        # Verify the new article is displayed
        self.assertIn(new_article, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test accessing and posting in the community forum
        self.login("admin", "admin123")

        # Access the forum
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the forum to load

        # Verify forum topics are displayed
        forum_posts = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming forum posts are in <li> elements
        self.assertGreater(len(forum_posts), 0, "No forum posts found.")

        # Post a new question
        new_question = "What are your favorite eco-friendly products?"
        self.driver.find_element(By.NAME, 'new_question').send_keys(new_question)  # Assuming there's an input for new questions
        self.driver.find_element(By.XPATH, '//button[text()="Post Question"]').click()
        time.sleep(1)  # Wait for the question to be posted

        # Verify the new question is displayed
        self.assertIn(new_question, self.driver.page_source)

    def test_logout_functionality(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
