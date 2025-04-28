import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8404/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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
        self.assertIn("Home", self.driver.title)  # Check if redirected to Home Page

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
        self.assertIn("Register", self.driver.title)  # Check if Registration Page is loaded

        # Click back to Login Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Login').click()
        self.assertIn("Login", self.driver.title)  # Check if redirected back to Login Page

    def test_submit_recipe(self):
        # Functionalities 4: Test recipe submission functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Recipe').click()

        # Input recipe details
        self.driver.find_element(By.NAME, 'title').send_keys("New Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("Ingredient1, Ingredient2")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Step 1, Step 2")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Recipe"]').click()

        # Verify success message
        self.assertIn("Recipe submitted successfully!", self.driver.page_source)

    def test_browse_recipes(self):
        # Functionalities 5: Test recipe browsing functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()

        # Search for a recipe
        self.driver.find_element(By.NAME, 'keyword').send_keys("Pasta")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the recipe is displayed
        self.assertIn("Pasta", self.driver.page_source)

    def test_view_recipe_details(self):
        # Functionalities 6: Test viewing recipe details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()  # Click on the Pasta recipe

        # Verify the recipe details are displayed
        self.assertIn("Title: Pasta", self.driver.page_source)

    def test_navigate_from_browsing_to_home(self):
        # Functionalities 7: Test navigation from Recipe Browsing to Home Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()

        # Verify that the Home Page is loaded
        self.assertIn("Home", self.driver.title)

    def test_user_profile(self):
        # Functionalities 8: Test accessing User Profile Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()

        # Verify that the User Profile Page is loaded
        self.assertIn("User Profile", self.driver.title)

    def test_navigate_from_details_to_home(self):
        # Functionalities 10: Test navigation from Recipe Details to Home Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()  # Click on the Pasta recipe
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()

        # Verify that the Home Page is loaded
        self.assertIn("Home", self.driver.title)

if __name__ == '__main__':
    unittest.main()
