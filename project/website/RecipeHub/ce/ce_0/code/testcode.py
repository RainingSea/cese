import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8402/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        
        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 3: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        
        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

        # Click back to Login Page
        self.driver.back()
        
        # Verify that the Login Page has loaded
        self.assertIn("Login", self.driver.title)

    def test_submit_recipe(self):
        # Functionalities 4: Test recipe submission functionality
        self.login("admin", "admin123")
        
        self.driver.find_element(By.LINK_TEXT, 'Submit Recipe').click()

        # Input recipe details
        self.driver.find_element(By.NAME, 'title').send_keys("Test Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("Test Ingredients")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Test Instructions")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that the user is redirected to the Home Page
        self.assertIn("Home", self.driver.title)

    def test_browse_recipes(self):
        # Functionalities 5: Test recipe browsing functionality
        self.login("admin", "admin123")
        
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        
        # Verify that the recipe browsing page has loaded
        self.assertIn("Browse Recipes", self.driver.title)

    def test_view_recipe_details(self):
        # Functionalities 6: Test viewing recipe details
        self.login("admin", "admin123")
        
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        
        # Click on the first recipe link
        self.driver.find_element(By.XPATH, '//ul/li/a').click()
        
        # Verify that the recipe details page has loaded
        self.assertIn("Recipe Details", self.driver.title)

    def test_navigation_from_browsing_to_home(self):
        # Functionalities 7: Test navigation from Recipe Browsing to Home Page
        self.login("admin", "admin123")
        
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        
        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_user_profile_page(self):
        # Functionalities 8: Test User Profile Page access
        self.login("admin", "admin123")
        
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        
        # Verify that the User Profile Page has loaded
        self.assertIn("User Profile", self.driver.title)

    def test_navigation_from_recipe_details_to_home(self):
        # Functionalities 10: Test navigation from Recipe Details to Home Page
        self.login("admin", "admin123")
        
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.driver.find_element(By.XPATH, '//ul/li/a').click()  # Click on a recipe
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        
        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

if __name__ == '__main__':
    unittest.main()
