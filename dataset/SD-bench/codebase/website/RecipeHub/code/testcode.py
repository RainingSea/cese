import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8691/')

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
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Home Page
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

        # Click back or cancel
        self.driver.find_element(By.LINK_TEXT, 'Cancel').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected back to the Login Page
        self.assertIn("Login", self.driver.page_source)

    def test_recipe_submission(self):
        # Functionalities 4: Test recipe submission functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Recipe').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter valid recipe details
        self.driver.find_element(By.NAME, 'title').send_keys("Test Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("Test Ingredients")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Test Instructions")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the recipe is submitted successfully
        self.assertIn("Browse Recipes", self.driver.page_source)

    def test_recipe_browsing(self):
        # Functionalities 5: Test recipe browsing functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter a valid keyword to search for recipes
        self.driver.find_element(By.NAME, 'search').send_keys("Pancakes")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify that the software displays a list of recipes matching the keyword
        self.assertIn("Pancakes", self.driver.page_source)

    def test_view_recipe_details(self):
        # Functionalities 6: Test viewing recipe details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Select a recipe from the browsing list
        self.driver.find_element(By.LINK_TEXT, 'Pancakes').click()
        time.sleep(1)  # Wait for the recipe details page to load

        # Verify that the user navigates to the Recipe Details Page
        self.assertIn("flour,milk,eggs", self.driver.page_source)

    def test_navigation_from_recipe_browsing_to_home(self):
        # Functionalities 7: Test navigation from Recipe Browsing to Home Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the Back to Home button
        self.driver.find_element(By.LINK_TEXT, 'Home').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the user is redirected back to the Home Page
        self.assertIn("Browse Recipes", self.driver.page_source)

    def test_user_profile_page(self):
        # Functionalities 8: Test accessing the User Profile Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # Verify that the user sees their profile information
        self.assertIn("admin", self.driver.page_source)

    def test_account_deletion(self):
        # Functionalities 9: Test account deletion functionality
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        # Click on the delete account option
        self.driver.find_element(By.XPATH, '//button[text()="Delete Account"]').click()
        time.sleep(1)  # Wait for the account deletion

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.page_source)

    def test_navigation_from_recipe_details_to_home(self):
        # Functionalities 10: Test navigation from Recipe Details to Home Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Select a recipe from the browsing list
        self.driver.find_element(By.LINK_TEXT, 'Pancakes').click()
        time.sleep(1)  # Wait for the recipe details page to load

        # Click the Back to Home button
        self.driver.find_element(By.LINK_TEXT, 'Home').click()
        time.sleep(1)  # Wait for the home page to load

        # Verify that the user is redirected back to the Home Page
        self.assertIn("Browse Recipes", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
