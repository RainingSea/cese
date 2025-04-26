import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8192/') 

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
        self.driver.get('http://localhost:8192/register')
        
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

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8192/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that an error message is displayed
        self.assertIn("Registration failed. User already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8192/')
        
        # Verify that the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("News Articles", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8192/')
        self.login("admin", "wrongpassword")

        # Verify that an error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_dashboard_browse_categories(self):
        # Functionality 3: Browse News Categories on the Dashboard Page
        self.login("admin", "admin123")
        
        # Verify that the Dashboard Page shows articles
        articles = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(articles), 0, "No articles found.")

    def test_search_articles(self):
        # Functionality 4: Search for Specific Topics or Keywords
        self.login("admin", "admin123")
        
        # Enter a specific keyword in the search bar
        search_query = "Sports"
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys(search_query)
        search_box.submit()

        # Verify that articles related to the keyword are displayed
        self.assertIn("Sports Update", self.driver.page_source)

        # Search for a keyword that has no related articles
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.clear()
        search_box.send_keys("Nonexistent Topic")
        search_box.submit()

        # Verify that no articles were found
        self.assertIn("No articles found.", self.driver.page_source)

    def test_view_article_details(self):
        # Functionality 5: View Article Summaries in the News Feed
        self.login("admin", "admin123")
        
        # Click on the first article
        self.driver.find_element(By.XPATH, '//li[@class="list-group-item"]/a').click()

        # Verify that the Article Details Page is displayed
        self.assertIn("Article Details", self.driver.title)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
