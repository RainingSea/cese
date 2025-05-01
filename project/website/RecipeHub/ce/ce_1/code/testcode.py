import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestRecipeHubApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask application
        cls.process = subprocess.Popen(['python', 'main.py'])
        # Give the server time to start
        time.sleep(2)
        
    @classmethod
    def tearDownClass(cls):
        # Stop the Flask application
        cls.process.terminate()
    
    def setUp(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8559/login')
        self.wait = WebDriverWait(self.driver, 10)
    
    def tearDown(self):
        # Close the webdriver session
        self.driver.quit()
    
    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        # Wait for page to load
        self.wait.until(EC.title_contains('Home'))
    
    def test_1_user_login(self):
        """Functionalities 1: User Login"""
        # Test with valid credentials
        self.login("admin", "admin123")
        # Verify redirection to home page
        self.assertIn("Home", self.driver.title)
        # Verify username is displayed
        self.assertIn("Welcome to RecipeHub, admin!", self.driver.page_source)
    
    def test_2_user_registration(self):
        """Functionalities 2: User Registration"""
        # Go to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Register new user
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Verify redirection to home page
        self.wait.until(EC.title_contains('Home'))
        self.assertIn(f"Welcome to RecipeHub, {username}!", self.driver.page_source)
    
    def test_3_navigation_to_registration_page(self):
        """Functionalities 3: Navigation to Registration Page from Login Page"""
        # Click register link
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Verify on registration page
        self.assertIn("Register", self.driver.title)
        
        # Click back to login
        self.driver.find_element(By.LINK_TEXT, 'Login here').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Verify back on login page
        self.assertIn("Login", self.driver.title)
    
    def test_4_recipe_submission(self):
        """Functionalities 4: Recipe Submission"""
        # First login
        self.login("admin", "admin123")
        
        # Go to submit recipe page
        self.driver.find_element(By.LINK_TEXT, 'Submit a New Recipe').click()
        self.wait.until(EC.title_contains('Submit Recipe'))
        
        # Submit a recipe
        title = "Test Recipe " + str(int(time.time()))
        ingredients = "Ingredient 1\nIngredient 2"
        instructions = "Step 1\nStep 2\nStep 3"
        
        self.driver.find_element(By.ID, 'title').send_keys(title)
        self.driver.find_element(By.ID, 'ingredients').send_keys(ingredients)
        self.driver.find_element(By.ID, 'instructions').send_keys(instructions)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Recipe"]').click()
        
        # Verify redirection to home page
        self.wait.until(EC.title_contains('Home'))
        
        # Verify recipe appears in profile
        self.driver.find_element(By.LINK_TEXT, 'My Profile').click()
        self.wait.until(EC.title_contains('Profile'))
        self.assertIn(title, self.driver.page_source)
    
    def test_5_recipe_browsing(self):
        """Functionalities 5: Recipe Browsing"""
        # First login
        self.login("admin", "admin123")
        
        # Go to browse recipes page
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.wait.until(EC.title_contains('Browse Recipes'))
        
        # Search for recipes
        search_term = "Test"
        search_box = self.driver.find_element(By.NAME, 'search')
        search_box.send_keys(search_term)
        search_box.submit()
        
        # Verify search results
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'recipe-item')))
        recipes = self.driver.find_elements(By.CLASS_NAME, 'recipe-item')
        self.assertGreater(len(recipes), 0, "No recipes found")
    
    def test_6_view_recipe_details(self):
        """Functionalities 6: View Recipe Details"""
        # First login
        self.login("admin", "admin123")
        
        # Go to browse recipes page
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.wait.until(EC.title_contains('Browse Recipes'))
        
        # Click on first recipe
        first_recipe = self.driver.find_element(By.CLASS_NAME, 'recipe-item')
        recipe_title = first_recipe.find_element(By.CLASS_NAME, 'recipe-title').text
        first_recipe.find_element(By.CLASS_NAME, 'view-btn').click()
        
        # Verify recipe details page
        self.wait.until(EC.title_contains(recipe_title))
        self.assertIn(recipe_title, self.driver.page_source)
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'ingredients-list').is_displayed())
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'instructions-text').is_displayed())
    
    def test_7_navigation_from_browsing_to_home(self):
        """Functionalities 7: Navigation from Recipe Browsing to Home Page"""
        # First login
        self.login("admin", "admin123")
        
        # Go to browse recipes page
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.wait.until(EC.title_contains('Browse Recipes'))
        
        # Click back to home
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        self.wait.until(EC.title_contains('Home'))
        
        # Verify on home page
        self.assertIn("Welcome to RecipeHub, admin!", self.driver.page_source)
    
    def test_8_user_profile_page(self):
        """Functionalities 8: User Profile Page"""
        # First login
        self.login("admin", "admin123")
        
        # Go to profile page
        self.driver.find_element(By.LINK_TEXT, 'My Profile').click()
        self.wait.until(EC.title_contains('Profile'))
        
        # Verify profile information
        self.assertIn("admin", self.driver.page_source)
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'recipe-list').is_displayed())
    
    def test_9_account_deletion(self):
        """Functionalities 9: Account Deletion"""
        # First create a test account
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.title_contains('Home'))
        
        # Go to profile page
        self.driver.find_element(By.LINK_TEXT, 'My Profile').click()
        self.wait.until(EC.title_contains('Profile'))
        
        # Delete account
        self.driver.find_element(By.XPATH, '//button[text()="Delete Account"]').click()
        
        # Verify redirection to login page
        self.wait.until(EC.title_contains('Login'))
        
        # Verify account is deleted by trying to login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
        self.assertIn("Invalid credentials", self.driver.page_source)
    
    def test_10_navigation_from_details_to_home(self):
        """Functionalities 10: Navigation from Recipe Details to Home Page"""
        # First login
        self.login("admin", "admin123")
        
        # Go to browse recipes page
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.wait.until(EC.title_contains('Browse Recipes'))
        
        # Click on first recipe
        first_recipe = self.driver.find_element(By.CLASS_NAME, 'recipe-item')
        first_recipe.find_element(By.CLASS_NAME, 'view-btn').click()
        self.wait.until(EC.title_contains('Recipe Details'))
        
        # Click back to home
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        self.wait.until(EC.title_contains('Home'))
        
        # Verify on home page
        self.assertIn("Welcome to RecipeHub, admin!", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
