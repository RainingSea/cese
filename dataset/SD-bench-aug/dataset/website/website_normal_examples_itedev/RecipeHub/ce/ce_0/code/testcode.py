import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/login')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()  # Terminate the Flask app process

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
        # Test user login functionality
        self.login("user1", "password1")
        self.assertIn("Welcome to RecipeHub", self.driver.page_source)

    def test_registration(self):
        # Test user registration functionality
        self.driver.get('http://localhost:5000/register')
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_to_registration(self):
        # Test navigation to the Registration Page
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

        # Click back to login
        self.driver.get('http://localhost:5000/login')
        time.sleep(1)  # Wait for the login page to load
        self.assertIn("Login", self.driver.title)

    def test_recipe_submission(self):
        # Test recipe submission functionality
        self.login("user1", "password1")
        self.driver.get('http://localhost:5000/recipe_submission')
        time.sleep(1)  # Wait for the recipe submission page to load

        # Input recipe details
        self.driver.find_element(By.NAME, 'title').send_keys("New Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("ingredient1|ingredient2")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Instructions for the recipe.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Recipe"]').click()
        time.sleep(1)  # Wait for the submission to complete

        # Verify that the recipe submission was successful
        self.assertIn("Browse Recipes", self.driver.page_source)

    def test_recipe_browsing(self):
        # Test recipe browsing functionality
        self.login("user1", "password1")
        self.driver.get('http://localhost:5000/recipe_browsing')
        time.sleep(1)  # Wait for the recipe browsing page to load

        # Search for a recipe
        self.driver.find_element(By.NAME, 'keyword').send_keys("Pasta")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that the search results are displayed
        self.assertIn("Pasta", self.driver.page_source)

    def test_user_profile(self):
        # Test user profile page access
        self.login("user1", "password1")
        self.driver.get('http://localhost:5000/user_profile/user1')
        time.sleep(1)  # Wait for the user profile page to load

        # Verify that the user profile page shows the user's recipes
        self.assertIn("Your Submitted Recipes", self.driver.page_source)

    def test_account_deletion(self):
        # Test account deletion functionality
        self.login("user1", "password1")
        self.driver.get('http://localhost:5000/user_profile/user1')
        time.sleep(1)  # Wait for the user profile page to load

        # Delete account
        self.driver.find_element(By.XPATH, '//button[text()="Delete Account"]').click()
        time.sleep(1)  # Wait for the deletion to complete

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
