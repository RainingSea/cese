import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8176/login')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "pass123")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
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

        # Navigate back to the Login Page
        self.driver.find_element(By.LINK_TEXT, 'Login').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Login Page has loaded
        self.assertIn("Login", self.driver.title)

    def test_recipe_submission(self):
        # Functionalities 4: Test recipe submission functionality
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Recipe').click()
        time.sleep(1)  # Wait for the next page to load

        # Enter recipe details
        self.driver.find_element(By.ID, 'title').send_keys("Test Recipe")
        self.driver.find_element(By.ID, 'ingredients').send_keys("Test Ingredients")
        self.driver.find_element(By.ID, 'instructions').send_keys("Test Instructions")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Recipe"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Recipe Browsing Page has loaded
        self.assertIn("Browse Recipes", self.driver.title)

    def test_recipe_browsing(self):
        # Functionalities 5: Test recipe browsing functionality
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Search for a recipe
        search_box = self.driver.find_element(By.NAME, 'search')
        search_box.send_keys("Pasta")
        search_box.submit()
        time.sleep(1)  # Wait for the search results to load

        # Verify that the search results contain the expected recipe
        self.assertIn("Pasta", self.driver.page_source)

    def test_view_recipe_details(self):
        # Functionalities 6: Test viewing recipe details
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on a recipe to view details
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()
        time.sleep(1)  # Wait for the recipe details to load

        # Verify that the Recipe Details Page has loaded
        self.assertIn("Pasta", self.driver.title)

    def test_navigation_from_recipe_browsing_to_home(self):
        # Functionalities 7: Test navigation from Recipe Browsing to Home Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Navigate back to the Home Page
        self.driver.find_element(By.LINK_TEXT, 'Home').click()
        time.sleep(1)  # Wait for the Home Page to load

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_user_profile_page(self):
        # Functionalities 8: Test accessing the User Profile Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)  # Wait for the User Profile Page to load

        # Verify that the User Profile Page has loaded
        self.assertIn("User Profile", self.driver.title)

    def test_account_deletion(self):
        # Functionalities 9: Test account deletion functionality
        self.fail("Account deletion functionality not implemented")

    def test_navigation_from_recipe_details_to_home(self):
        # Functionalities 10: Test navigation from Recipe Details to Home Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on a recipe to view details
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()
        time.sleep(1)  # Wait for the recipe details to load

        # Navigate back to the Home Page
        self.driver.find_element(By.LINK_TEXT, 'Home').click()
        time.sleep(1)  # Wait for the Home Page to load

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

if __name__ == '__main__':
    unittest.main()
