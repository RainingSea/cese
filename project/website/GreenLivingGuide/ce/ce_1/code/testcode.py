import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestGreenLivingGuide(unittest.TestCase):

    def setUp(self):
        # Start the server and initialize the webdriver
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/login.html')  # Adjusted to the correct login page

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_view_sustainable_living_intro(self):
        # Functionalities 4: Test viewing introduction after logging in
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/introduction.html')  # Assuming this is the intro page
        self.assertIn("Introduction to Sustainable Living", self.driver.page_source)

    def test_view_and_submit_tips(self):
        # Functionalities 5: Test viewing and submitting sustainable living tips
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/tips.html')  # Assuming this is the tips page

        # Verify existing tips are displayed
        self.assertIn("Reduce, reuse, recycle.", self.driver.page_source)

        # Submit a new tip
        self.driver.find_element(By.NAME, 'tip').send_keys("Use public transport.")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the tip to be submitted

        # Verify the new tip is displayed
        self.assertIn("Use public transport.", self.driver.page_source)

    def test_read_and_submit_articles(self):
        # Functionalities 6: Test reading and submitting articles
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/articles.html')  # Assuming this is the articles page

        # Verify existing articles are displayed
        self.assertIn("The Importance of Sustainable Living.", self.driver.page_source)

        # Submit a new article
        self.driver.find_element(By.NAME, 'article').send_keys("New Article on Sustainability.")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the article to be submitted

        # Verify the new article is displayed
        self.assertIn("New Article on Sustainability.", self.driver.page_source)

    def test_participate_in_forum(self):
        # Functionalities 7: Test accessing and posting in the community forum
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/forum.html')  # Assuming this is the forum page

        # Verify forum posts are displayed
        self.assertIn("What are your favorite sustainable living tips?", self.driver.page_source)

        # Post a new question
        self.driver.find_element(By.NAME, 'post').send_keys("What are the best eco-friendly products?")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the post to be submitted

        # Verify the new post is displayed
        self.assertIn("What are the best eco-friendly products?", self.driver.page_source)

    def test_navigation_to_other_sections(self):
        # Functionalities 8: Test navigation to other sections
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8000/articles.html')  # Navigate to articles
        self.assertIn("Articles", self.driver.page_source)

        self.driver.get('http://localhost:8000/tips.html')  # Navigate to tips
        self.assertIn("Sustainable Living Tips", self.driver.page_source)

    def test_logout_functionality(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
