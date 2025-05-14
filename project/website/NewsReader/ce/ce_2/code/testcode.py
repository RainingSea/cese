import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestNewsReaderApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app in a separate process
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8093/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the web driver session and terminate the Flask process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
        password_field = self.driver.find_element(By.ID, 'password')
        login_button = self.driver.find_element(By.XPATH, '//button[text()="Login"]')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        self.wait.until(EC.title_contains("Dashboard"))

    def test_user_registration(self):
        """Test Functionality 1: User Registration"""
        # Navigate to registration page
        register_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Register')))
        register_link.click()
        self.wait.until(EC.title_contains("Register"))

        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        
        username_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')
        register_button = self.driver.find_element(By.XPATH, '//button[text()="Register"]')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        register_button.click()
        
        # Verify redirect to login page with success message
        self.wait.until(EC.title_contains("Login"))
        flash_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alert-success')))
        self.assertIn("Registration successful", flash_message.text)

        # Test registration with existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains("Register"))
        
        username_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')
        register_button = self.driver.find_element(By.XPATH, '//button[text()="Register"]')
        
        username_field.send_keys("admin")  # Existing username
        password_field.send_keys("anypassword")
        register_button.click()
        
        # Verify error message
        flash_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger')))
        self.assertIn("Username already exists", flash_message.text)

    def test_user_login(self):
        """Test Functionality 2: User Login"""
        # Test successful login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        
        # Verify username is displayed
        username_display = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="header"]/div/span')))
        self.assertIn("admin", username_display.text)
        
        # Logout to test invalid login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains("Login"))
        
        # Test invalid login
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
        password_field = self.driver.find_element(By.ID, 'password')
        login_button = self.driver.find_element(By.XPATH, '//button[text()="Login"]')
        
        username_field.send_keys("invalid")
        password_field.send_keys("credentials")
        login_button.click()
        
        # Verify error message
        flash_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger')))
        self.assertIn("Invalid username or password", flash_message.text)

    def test_browse_news_categories(self):
        """Test Functionality 3: Browse News Categories"""
        self.login("admin", "admin123")
        
        # Verify categories are displayed
        categories = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'category-list')))
        self.assertGreater(len(categories), 0)
        
        # Test clicking a category
        sports_link = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "sports")]')))
        sports_link.click()
        
        # Verify URL contains category parameter
        self.wait.until(EC.url_contains("category=sports"))
        
        # Verify articles are filtered
        articles = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article-card')))
        for article in articles:
            meta = article.find_element(By.CLASS_NAME, 'meta')
            self.assertIn("sports", meta.text)

    def test_search_articles(self):
        """Test Functionality 4: Search Articles"""
        self.login("admin", "admin123")
        
        # Verify search bar is present
        search_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'query')))
        self.assertTrue(search_input.is_displayed())
        
        # Test search with existing keyword
        search_input.send_keys("Tech")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify search results
        self.wait.until(EC.url_contains("query=Tech"))
        articles = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article-card')))
        self.assertGreater(len(articles), 0)
        
        # Test search with non-existing keyword
        search_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'query')))
        search_input.clear()
        search_input.send_keys("nonexistentkeyword")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify no results message
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "No articles found")]')))

    def test_view_article_summaries(self):
        """Test Functionality 5: View Article Summaries"""
        self.login("admin", "admin123")
        
        # Verify articles are displayed with summaries
        articles = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article-card')))
        self.assertGreater(len(articles), 0)
        
        for article in articles:
            title = article.find_element(By.TAG_NAME, 'h3')
            summary = article.find_element(By.TAG_NAME, 'p')
            self.assertTrue(title.text)
            self.assertTrue(summary.text)
        
        # Test clicking an article
        first_article = articles[0]
        article_title = first_article.find_element(By.TAG_NAME, 'h3').text
        first_article.find_element(By.TAG_NAME, 'a').click()
        
        # Verify article details page
        self.wait.until(EC.title_contains(article_title))
        content = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'article-content')))
        self.assertTrue(content.text)

    def test_user_logout(self):
        """Test Functionality 6: User Logout"""
        self.login("admin", "admin123")
        
        # Test logout
        logout_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Logout')))
        logout_link.click()
        
        # Verify redirect to login page
        self.wait.until(EC.title_contains("Login"))
        
        # Test accessing dashboard after logout
        self.driver.get('http://localhost:8093/dashboard')
        
        # Verify redirect back to login page
        self.wait.until(EC.title_contains("Login"))

if __name__ == '__main__':
    unittest.main()
