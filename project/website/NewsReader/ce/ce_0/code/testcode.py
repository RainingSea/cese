import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8305/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8305/register')
        
        # Check if registration page is displayed
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Expectation: The user is registered successfully, and a confirmation message is displayed
        # (Assuming a confirmation message is shown on the page)
        self.assertIn("Registration successful", self.driver.page_source)

        # Attempt to register with an already existing username
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Expectation: An error message is displayed indicating that the username is already taken
        self.assertIn("Username already taken", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8305/')

        # Check if login page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Expectation: Access is granted, and the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.login("invalid_user", "wrong_password")

        # Expectation: An error message is displayed indicating that the credentials are incorrect
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_browse_news_categories(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Expectation: A list of news categories is displayed
        categories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(categories), 0, "No categories found.")

        # Click on a specific news category
        categories[0].click()

        # Expectation: The user is shown a list of articles related to the selected category
        self.assertIn("Articles", self.driver.page_source)

    def test_search_for_specific_topics(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Expectation: The search bar is visible on the Dashboard Page
        search_bar = self.driver.find_element(By.NAME, 'keyword')
        self.assertIsNotNone(search_bar)

        # Enter a specific keyword in the search bar and submit
        search_bar.send_keys("Olympics")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Expectation: A list of articles related to the keyword is displayed
        self.assertIn("Olympics", self.driver.page_source)

        # Enter a keyword that has no related articles
        search_bar.clear()
        search_bar.send_keys("NonExistentKeyword")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Expectation: A message is displayed indicating that no articles were found
        self.assertIn("No articles found", self.driver.page_source)

    def test_view_article_summaries(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Expectation: A list of articles with headlines, summaries, and sources is displayed
        articles = self.driver.find_elements(By.CLASS_NAME, 'article-summary')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Click on an article headline
        articles[0].click()

        # Expectation: The user is redirected to the Article Details Page displaying the full text of the article
        self.assertIn("Article Details", self.driver.title)

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Logout from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Expectation: The user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page after logging out
        self.driver.get('http://localhost:8305/dashboard')

        # Expectation: The user is redirected to the Login Page, and access to the Dashboard is denied
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
