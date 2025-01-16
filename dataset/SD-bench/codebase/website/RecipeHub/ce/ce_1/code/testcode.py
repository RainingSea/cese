import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server some time to start
        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8687/') 

    def tearDown(self):
        # Close the web driver session and stop the application
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
        self.login("admin", "admin123")
        # Verify that the user is redirected to the Recipe Browsing Page
        self.assertIn("Browse Recipes", self.driver.page_source)

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
        self.assertIn("Login", self.driver.page_source)

    def test_navigation_to_registration_page(self):
        # Functionalities 3: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.page_source)

        # Test navigation back to the Login Page
        self.driver.find_element(By.LINK_TEXT, 'Login').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.page_source)

    def test_recipe_submission(self):
        # Functionalities 4: Test recipe submission functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit a Recipe').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.NAME, 'title').send_keys("Test Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("Test Ingredients")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Test Instructions")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Recipe"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the recipe is submitted successfully
        self.assertIn("Browse Recipes", self.driver.page_source)

    def test_recipe_browsing(self):
        # Functionalities 5: Test recipe browsing functionality
        self.login("admin", "admin123")
        # Verify that recipes are displayed
        recipes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recipes), 0, "No recipes found.")

    def test_view_recipe_details(self):
        # Functionalities 6: Test viewing recipe details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Test Recipe').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Recipe Details Page has loaded
        self.assertIn("Test Recipe", self.driver.page_source)

    def test_navigation_from_recipe_browsing_to_home(self):
        # Functionalities 7: Test navigation from Recipe Browsing to Home Page
        self.fail("Not implemented")

    def test_user_profile_page(self):
        # Functionalities 8: Test accessing the User Profile Page
        self.fail("Not implemented")

    def test_account_deletion(self):
        # Functionalities 9: Test account deletion
        self.fail("Not implemented")

    def test_navigation_from_recipe_details_to_home(self):
        # Functionalities 10: Test navigation from Recipe Details to Home Page
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
