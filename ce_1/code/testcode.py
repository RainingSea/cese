import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'], cwd='ce_1/code')
        time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8168')

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
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_navigation_to_registration_page(self):
        # Functionalities 3: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

        # Test navigation back to Login Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Login').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Login", self.driver.title)

    def test_recipe_submission(self):
        # Functionalities 4: Test recipe submission functionality
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Recipe').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.NAME, 'title').send_keys("Test Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("Test Ingredients")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Test Instructions")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Recipe"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Home", self.driver.title)

    def test_recipe_browsing(self):
        # Functionalities 5: Test recipe browsing functionality
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.NAME, 'keyword').send_keys("Test")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        recipes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recipes), 0, "No recipes found.")

    def test_view_recipe_details(self):
        # Functionalities 6: Test viewing recipe details
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.NAME, 'keyword').send_keys("Test")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        self.driver.find_element(By.LINK_TEXT, 'Test Recipe').click()
        time.sleep(1)  # Wait for the recipe details to load

        self.assertIn("Recipe Details", self.driver.title)

    def test_navigation_from_recipe_browsing_to_home(self):
        # Functionalities 7: Test navigation from Recipe Browsing to Home Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn("Home", self.driver.title)

    def test_user_profile_page(self):
        # Functionalities 8: Test access to User Profile Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        self.assertIn("User Profile", self.driver.title)

    def test_account_deletion(self):
        # Functionalities 9: Test account deletion
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)  # Wait for the profile page to load

        self.driver.find_element(By.XPATH, '//button[text()="Delete Account"]').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_navigation_from_recipe_details_to_home(self):
        # Functionalities 10: Test navigation from Recipe Details to Home Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.NAME, 'keyword').send_keys("Test")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        self.driver.find_element(By.LINK_TEXT, 'Test Recipe').click()
        time.sleep(1)  # Wait for the recipe details to load

        self.driver.find_element(By.LINK_TEXT, 'Back to Browsing').click()
        time.sleep(1)  # Wait for the browsing page to load

        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn("Home", self.driver.title)

if __name__ == '__main__':
    unittest.main()
