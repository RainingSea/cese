import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8149')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "pass123")
        # Verify that the Home Page has loaded
        self.assertIn("Welcome to RecipeHub!", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigation_to_registration_page(self):
        # Functionalities 3: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

        # Click back to login page
        self.driver.find_element(By.LINK_TEXT, 'Back to Login').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Login Page has loaded
        self.assertIn("Login", self.driver.title)

    def test_recipe_submission(self):
        # Functionalities 4: Test recipe submission functionality
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Recipe').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the recipe submission form
        self.driver.find_element(By.NAME, 'title').send_keys("Test Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("ingredient1, ingredient2")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Mix ingredients.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Recipe"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify success message
        self.assertIn("Recipe submitted successfully!", self.driver.page_source)

    def test_recipe_browsing(self):
        # Functionalities 5: Test recipe browsing functionality
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Search for a recipe
        self.driver.find_element(By.NAME, 'keyword').send_keys("Pasta")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that the recipe is displayed
        self.assertIn("Pasta", self.driver.page_source)

    def test_view_recipe_details(self):
        # Functionalities 6: Test viewing recipe details
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on a recipe to view details
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()
        time.sleep(1)  # Wait for the details page to load

        # Verify that the recipe details are displayed
        self.assertIn("Pasta", self.driver.page_source)
        self.assertIn("Boil pasta and mix with sauce.", self.driver.page_source)

    def test_navigation_from_browsing_to_home(self):
        # Functionalities 7: Test navigation from Recipe Browsing to Home Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click back to home
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the Home Page has loaded
        self.assertIn("Welcome to RecipeHub!", self.driver.page_source)

    def test_user_profile_page(self):
        # Functionalities 8: Test access to User Profile Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the user profile information is displayed
        self.assertIn("Your Profile", self.driver.page_source)

    def test_account_deletion(self):
        # Functionalities 9: Test account deletion functionality
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # Delete account
        self.driver.find_element(By.XPATH, '//button[text()="Delete Account"]').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigation_from_details_to_home(self):
        # Functionalities 10: Test navigation from Recipe Details to Home Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on a recipe to view details
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()
        time.sleep(1)  # Wait for the details page to load

        # Click back to browsing
        self.driver.find_element(By.LINK_TEXT, 'Back to Browsing').click()
        time.sleep(1)  # Wait for the browsing page to load

        # Click back to home
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the Home Page has loaded
        self.assertIn("Welcome to RecipeHub!", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
