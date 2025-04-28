import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestGreenLivingGuideApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8334/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_view_and_submit_tips(self):
        # Functionalities 5: View existing sustainable living tips and submit a new tip
        self.login("admin", "admin123")

        # View existing tips
        self.driver.get('http://localhost:8334/submit_tip')
        tips = self.driver.find_elements(By.TAG_NAME, 'textarea')
        self.assertGreater(len(tips), 0, "No tips found.")

        # Submit a new tip
        new_tip = "Reduce plastic use"
        self.driver.find_element(By.NAME, 'tip').send_keys(new_tip)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify the new tip is displayed
        self.driver.get('http://localhost:8334/dashboard')
        self.assertIn(new_tip, self.driver.page_source)

    def test_view_and_submit_articles(self):
        # Functionalities 6: View existing articles and submit a new article
        self.login("admin", "admin123")

        # View existing articles
        self.driver.get('http://localhost:8334/submit_article')
        articles = self.driver.find_elements(By.TAG_NAME, 'textarea')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Submit a new article
        new_article = "New Sustainable Living Practices"
        self.driver.find_element(By.NAME, 'article').send_keys(new_article)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify the new article is displayed
        self.driver.get('http://localhost:8334/dashboard')
        self.assertIn(new_article, self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Access the community forum and post a new question
        self.login("admin", "admin123")

        # Access the forum
        self.driver.get('http://localhost:8334/forum')
        self.assertIn("Community Forum", self.driver.title)

        # Post a new question
        new_post = "What are some eco-friendly practices?"
        self.driver.find_element(By.NAME, 'post').send_keys(new_post)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify the new post is visible
        self.assertIn(new_post, self.driver.page_source)

    def test_logout_functionality(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
