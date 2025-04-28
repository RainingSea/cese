import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8355/') 

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8355/register')
        
        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.get('http://localhost:8355/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message is displayed
        self.assertIn("Username already exists", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8355/')
        
        # Verify that the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8355/')
        self.login("admin", "wrongpassword")

        # Verify error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_browse_news_categories(self):
        # Functionality 3: Browse News Categories on the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows categories
        self.assertIn("Dashboard", self.driver.title)
        categories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(categories), 0, "No categories found.")

        # Click on a specific news category (assuming the first one is valid)
        self.driver.find_element(By.XPATH, '//ul/li[1]/a').click()

        # Verify that the article details page is displayed
        self.assertIn("article", self.driver.current_url)

    def test_view_article_summaries(self):
        # Functionality 5: View Article Summaries in the News Feed
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows articles
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found.")

        # Click on an article headline
        self.driver.find_element(By.XPATH, '//ul/li[1]/a').click()

        # Verify that the Article Details Page is displayed
        self.assertIn("article", self.driver.current_url)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.get('http://localhost:8355/dashboard')
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to navigate back to the Dashboard Page after logging out
        self.driver.get('http://localhost:8355/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
