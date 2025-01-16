import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\codebase\\website\\RecipeHub\\code')
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8550/')

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

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

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

        # Test navigation back to the Login Page
        self.driver.back()
        time.sleep(1)  # Wait for the page to load
        self.assertIn("Login", self.driver.title)

    def test_recipe_submission(self):
        # Functionalities 4: Test recipe submission functionality
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Recipe').click()
        time.sleep(1)  # Wait for the next page to load

        # Input recipe details
        self.driver.find_element(By.NAME, 'title').send_keys("Test Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("Test Ingredients")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Test Instructions")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_recipe_browsing(self):
        # Functionalities 5: Test recipe browsing functionality
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Search for a recipe
        self.driver.find_element(By.NAME, 'keyword').send_keys("Pasta")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify that the recipe is displayed
        self.assertIn("Pasta", self.driver.page_source)

    def test_view_recipe_details(self):
        # Functionalities 6: Test viewing recipe details
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on a recipe to view details
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()
        time.sleep(1)  # Wait for the page to load

        # Verify that the Recipe Details Page has loaded
        self.assertIn("Pasta", self.driver.title)

    def test_navigation_from_browsing_to_home(self):
        # Functionalities 7: Test navigation from Recipe Browsing to Home Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Navigate back to Home Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the page to load

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_user_profile_page(self):
        # Functionalities 8: Test accessing the User Profile Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)  # Wait for the page to load

        # Verify that the User Profile Page has loaded
        self.assertIn("User Profile", self.driver.title)

    def test_account_deletion(self):
        # Functionalities 9: Test account deletion
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)  # Wait for the page to load

        # Delete account
        self.driver.find_element(By.XPATH, '//button[text()="Delete Account"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigation_from_recipe_details_to_home(self):
        # Functionalities 10: Test navigation from Recipe Details to Home Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on a recipe to view details
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()
        time.sleep(1)  # Wait for the page to load

        # Navigate back to Home Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the page to load

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

if __name__ == '__main__':
    unittest.main()
