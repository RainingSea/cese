import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:/Project/Datasets/SD-bench/codebase/website/RecipeHub/code')
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/login')

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
        # Test case for user login
        self.login("user1", "password1")
        self.assertNotIn("Login", self.driver.title)

    def test_user_registration(self):
        # Test case for user registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_navigation_to_registration_page(self):
        # Test case for navigation to the registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)

        self.driver.back()
        time.sleep(1)  # Wait for the previous page to load
        self.assertIn("Login", self.driver.title)

    def test_recipe_submission(self):
        # Test case for recipe submission
        self.login("user1", "password1")
        self.driver.get('http://localhost:5000/recipe_submission')
        self.driver.find_element(By.NAME, 'title').send_keys("Test Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("ingredient1|ingredient2")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Test instructions")
        self.driver.find_element(By.XPATH, '//button[text()="Submit Recipe"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Browse Recipes", self.driver.title)

    def test_recipe_browsing(self):
        # Test case for recipe browsing
        self.login("user1", "password1")
        self.driver.get('http://localhost:5000/recipe_browsing')
        self.driver.find_element(By.NAME, 'keyword').send_keys("Pasta")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        recipes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recipes), 0, "No recipes found.")

    def test_view_recipe_details(self):
        # Test case for viewing recipe details
        self.fail("not implemented")

    def test_navigation_from_recipe_browsing_to_home(self):
        # Test case for navigation from recipe browsing to home page
        self.login("user1", "password1")
        self.driver.get('http://localhost:5000/recipe_browsing')
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)  # Wait for the home page to load

        self.assertIn("Welcome to RecipeHub", self.driver.page_source)

    def test_user_profile_page(self):
        # Test case for accessing the user profile page
        self.login("user1", "password1")
        self.driver.get('http://localhost:5000/user_profile')
        self.assertIn("User Profile", self.driver.page_source)

    def test_account_deletion(self):
        # Test case for account deletion
        self.login("user1", "password1")
        self.driver.get('http://localhost:5000/user_profile')
        self.driver.find_element(By.XPATH, '//button[text()="Delete Account"]').click()
        time.sleep(1)  # Wait for the redirection

        self.assertIn("Login", self.driver.title)

    def test_navigation_from_recipe_details_to_home(self):
        # Test case for navigation from recipe details to home page
        self.fail("not implemented")

if __name__ == '__main__':
    unittest.main()
