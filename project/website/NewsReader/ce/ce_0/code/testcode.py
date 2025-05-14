import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestNewsReaderApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the Flask application
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask application
        cls.process.terminate()

    def setUp(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8091/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()

    def login(self, username, password):
        """Helper method to perform login"""
        self.driver.get('http://localhost:8091/login')
        self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains('Dashboard'))

    def test_functionality_1_user_registration(self):
        """Test user registration functionality"""
        # Navigate to registration page
        self.driver.get('http://localhost:8091/register')
        self.wait.until(EC.title_contains('Register'))
        
        # Test case 1: Verify registration page elements
        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')
        submit_button = self.driver.find_element(By.XPATH, '//button[text()="Register"]')
        self.assertTrue(username_field.is_displayed())
        self.assertTrue(password_field.is_displayed())
        self.assertTrue(submit_button.is_displayed())

        # Test case 2: Register new user
        username_field.send_keys("newuser")
        password_field.send_keys("newpass123")
        submit_button.click()
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

        # Test case 3: Attempt to register existing user
        self.driver.get('http://localhost:8091/register')
        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')
        submit_button = self.driver.find_element(By.XPATH, '//button[text()="Register"]')
        username_field.send_keys("admin")  # Existing user
        password_field.send_keys("password")
        submit_button.click()
        self.assertTrue(self.driver.current_url.endswith('/register'))

    def test_functionality_2_user_login(self):
        """Test user login functionality"""
        # Test case 1: Verify login page elements
        self.driver.get('http://localhost:8091/login')
        self.wait.until(EC.title_contains('Login'))
        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')
        submit_button = self.driver.find_element(By.XPATH, '//button[text()="Login"]')
        self.assertTrue(username_field.is_displayed())
        self.assertTrue(password_field.is_displayed())
        self.assertTrue(submit_button.is_displayed())

        # Test case 2: Successful login
        self.login("admin", "admin123")
        self.assertIn('Dashboard', self.driver.title)

        # Logout for next test
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))

        # Test case 3: Failed login
        self.driver.get('http://localhost:8091/login')
        self.driver.find_element(By.NAME, 'username').send_keys("wronguser")
        self.driver.find_element(By.NAME, 'password').send_keys("wrongpass")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertEqual(error_message, 'Invalid credentials')

    def test_functionality_3_browse_news_categories(self):
        """Test browsing news categories"""
        self.login("admin", "admin123")
        
        # Test case 1: Verify categories are displayed
        categories = self.driver.find_elements(By.CSS_SELECTOR, '.sidebar ul li a')
        self.assertGreater(len(categories), 0, "No categories found")
        
        # Get the expected categories from the file
        expected_categories = ['General', 'Technology', 'Sports', 'Business', 'Entertainment']
        
        # Test case 2: Verify all categories are present
        displayed_categories = [cat.text for cat in categories[1:]]  # Skip "All" link
        self.assertEqual(set(displayed_categories), set(expected_categories))
        
        # Test case 3: Click on a category and verify filtered news
        sports_link = self.driver.find_element(By.LINK_TEXT, 'Sports')
        sports_link.click()
        self.wait.until(EC.url_contains('category=Sports'))
        
        # Verify news items are filtered by category
        news_items = self.driver.find_elements(By.CLASS_NAME, 'news-card')
        for item in news_items:
            category = item.find_element(By.CLASS_NAME, 'category').text
            self.assertEqual(category, 'Sports')

    def test_functionality_4_search_news(self):
        """Test searching for news"""
        self.login("admin", "admin123")
        
        # Test case 1: Verify search bar is present
        search_bar = self.driver.find_element(By.NAME, 'query')
        self.assertTrue(search_bar.is_displayed())
        
        # Test case 2: Search for existing term
        search_bar.send_keys("Tech")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.wait.until(EC.url_contains('query=Tech'))
        
        news_items = self.driver.find_elements(By.CLASS_NAME, 'news-card')
        self.assertGreater(len(news_items), 0, "No news items found for search term")
        
        # Verify at least one item contains the search term
        found = False
        for item in news_items:
            title = item.find_element(By.TAG_NAME, 'h3').text
            summary = item.find_element(By.CLASS_NAME, 'summary').text
            if 'Tech' in title or 'Tech' in summary:
                found = True
                break
        self.assertTrue(found, "Search term not found in any news item")
        
        # Test case 3: Search for non-existing term
        search_bar = self.driver.find_element(By.NAME, 'query')
        search_bar.clear()
        search_bar.send_keys("NonexistentTerm123")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.wait.until(EC.url_contains('query=NonexistentTerm123'))
        
        news_items = self.driver.find_elements(By.CLASS_NAME, 'news-card')
        self.assertEqual(len(news_items), 0, "News items found for non-existent term")

    def test_functionality_5_view_article_summaries(self):
        """Test viewing article summaries and details"""
        self.login("admin", "admin123")
        
        # Test case 1: Verify news feed with summaries is displayed
        news_items = self.driver.find_elements(By.CLASS_NAME, 'news-card')
        self.assertGreater(len(news_items), 0, "No news items found")
        
        # Verify each item has required elements
        for item in news_items:
            title = item.find_element(By.TAG_NAME, 'h3')
            summary = item.find_element(By.CLASS_NAME, 'summary')
            category = item.find_element(By.CLASS_NAME, 'category')
            source = item.find_element(By.CLASS_NAME, 'source')
            self.assertTrue(title.is_displayed())
            self.assertTrue(summary.is_displayed())
            self.assertTrue(category.is_displayed())
            self.assertTrue(source.is_displayed())
        
        # Test case 2: Click on an article and verify details page
        first_article_title = news_items[0].find_element(By.TAG_NAME, 'h3').text
        news_items[0].find_element(By.TAG_NAME, 'a').click()
        self.wait.until(EC.title_contains(first_article_title))
        
        # Verify article details page
        article_title = self.driver.find_element(By.TAG_NAME, 'h1').text
        article_content = self.driver.find_element(By.CLASS_NAME, 'article-content').text
        self.assertEqual(article_title, first_article_title)
        self.assertTrue(len(article_content) > 0, "Article content is empty")

    def test_functionality_6_user_logout(self):
        """Test user logout functionality"""
        self.login("admin", "admin123")
        
        # Test case 1: Logout from dashboard
        logout_link = self.driver.find_element(By.LINK_TEXT, 'Logout')
        logout_link.click()
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)
        
        # Test case 2: Attempt to access dashboard after logout
        self.driver.get('http://localhost:8091/dashboard')
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

if __name__ == '__main__':
    unittest.main()
