import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8231/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Verify redirection to Home Page

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 3: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)  # Verify Registration Page

        # Click back to Login Page
        self.driver.back()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)  # Verify Login Page

    def test_submit_recipe(self):
        # Functionalities 4: Test recipe submission
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit a Recipe').click()
        time.sleep(1)  # Wait for the next page to load

        # Fill out the recipe submission form
        self.driver.find_element(By.NAME, 'title').send_keys("New Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("Ingredient1, Ingredient2")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Instructions for the recipe.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the submission to complete

        # Verify success message
        self.assertIn("Recipe submitted successfully!", self.driver.page_source)

    def test_browse_recipes(self):
        # Functionalities 5: Test recipe browsing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Search for a recipe
        self.driver.find_element(By.NAME, 'query').send_keys("Pasta")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that the recipe is displayed
        self.assertIn("Pasta", self.driver.page_source)

    def test_view_recipe_details(self):
        # Functionalities 6: Test viewing recipe details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the recipe link
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()
        time.sleep(1)  # Wait for the recipe details page to load

        # Verify recipe details
        self.assertIn("Pasta", self.driver.page_source)
        self.assertIn("Pasta, Tomato Sauce, Cheese", self.driver.page_source)

    def test_navigate_from_browsing_to_home(self):
        # Functionalities 7: Test navigation from Recipe Browsing to Home Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the Back to Home button
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to Home Page
        self.assertIn("Home", self.driver.title)

    def test_user_profile_page(self):
        # Functionalities 8: Test accessing User Profile Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify User Profile Page
        self.assertIn("User Profile", self.driver.title)

    def test_delete_account(self):
        # Functionalities 9: Test account deletion
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the delete account button
        self.driver.find_element(By.XPATH, '//button[text()="Delete Account"]').click()
        time.sleep(1)  # Wait for the confirmation

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_from_recipe_details_to_home(self):
        # Functionalities 10: Test navigation from Recipe Details to Home Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the recipe link
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()
        time.sleep(1)  # Wait for the recipe details page to load

        # Click the Back to Home button
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to Home Page
        self.assertIn("Home", self.driver.title)

if __name__ == '__main__':
    unittest.main()
