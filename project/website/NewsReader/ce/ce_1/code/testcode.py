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
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8092/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.get('http://localhost:8092/login')
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.XPATH, '//button[text()="Login"]')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        self.wait.until(EC.title_contains('Dashboard'))

    # Functionality 1: User Registration
    def test_user_registration(self):
        # Test registration page display
        self.driver.get('http://localhost:8092/register')
        self.assertIn('Register', self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'password').is_displayed())
        
        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.title_contains('Login'))
        
        # Test duplicate username registration
        self.driver.get('http://localhost:8092/register')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')  # existing user
        self.driver.find_element(By.NAME, 'password').send_keys('password123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        error_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
        self.assertIn('Username already exists', error_message.text)

    # Functionality 2: User Login
    def test_user_login(self):
        # Test login page display
        self.driver.get('http://localhost:8092/login')
        self.assertIn('Login', self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'password').is_displayed())
        
        # Test successful login
        self.login('admin', 'admin123')
        self.assertIn('Dashboard', self.driver.title)
        
        # Test invalid login
        self.driver.get('http://localhost:8092/login')
        self.driver.find_element(By.NAME, 'username').send_keys('wronguser')
        self.driver.find_element(By.NAME, 'password').send_keys('wrongpass')
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        
        error_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
        self.assertIn('Invalid credentials', error_message.text)

    # Functionality 3: Browse News Categories
    def test_browse_news_categories(self):
        self.login('admin', 'admin123')
        
        # Verify categories are displayed
        categories = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.categories a')))
        self.assertGreater(len(categories), 0)
        
        # Test category filtering
        category_to_test = categories[1].text  # Get the first non-"All" category
        categories[1].click()
        
        # Wait for articles to load
        time.sleep(1)
        articles = self.driver.find_elements(By.CLASS_NAME, 'article')
        self.assertGreater(len(articles), 0)
        
        # Verify the selected category is active
        active_category = self.driver.find_element(By.CSS_SELECTOR, '.categories a.active')
        self.assertEqual(active_category.text, category_to_test)

    # Functionality 4: Search for Specific Topics
    def test_search_functionality(self):
        self.login('admin', 'admin123')
        
        # Verify search bar is visible
        search_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'query')))
        self.assertTrue(search_input.is_displayed())
        
        # Test successful search
        search_input.send_keys('Climate')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        articles = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article')))
        self.assertGreater(len(articles), 0)
        
        # Verify search results contain the keyword
        self.assertIn('Climate', articles[0].text)
        
        # Test search with no results
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.clear()
        search_input.send_keys('nonexistentkeyword')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        articles = self.driver.find_elements(By.CLASS_NAME, 'article')
        self.assertEqual(len(articles), 0)

    # Functionality 5: View Article Summaries
    def test_view_article_summaries(self):
        self.login('admin', 'admin123')
        
        # Verify articles are displayed with summaries
        articles = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article')))
        self.assertGreater(len(articles), 0)
        
        # Check each article has required elements
        for article in articles:
            self.assertTrue(article.find_element(By.TAG_NAME, 'h3').is_displayed())
            self.assertTrue(article.find_element(By.TAG_NAME, 'p').is_displayed())
            self.assertTrue(article.find_element(By.CLASS_NAME, 'meta').is_displayed())
        
        # Test viewing article details
        article_title = articles[0].find_element(By.TAG_NAME, 'h3').text
        articles[0].find_element(By.TAG_NAME, 'a').click()
        
        self.wait.until(EC.title_contains(article_title))
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'content').is_displayed())

    # Functionality 6: User Logout
    def test_user_logout(self):
        self.login('admin', 'admin123')
        
        # Test logout
        logout_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Logout')))
        logout_link.click()
        
        self.wait.until(EC.title_contains('Login'))
        
        # Test access to dashboard after logout
        self.driver.get('http://localhost:8092/dashboard')
        self.wait.until(EC.title_contains('Login'))

if __name__ == '__main__':
    unittest.main()
