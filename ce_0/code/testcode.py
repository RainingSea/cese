import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web app to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8167')

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
        # Functionalities 1: User Login
        self.login("admin", "pass123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_navigation_to_registration_page(self):
        # Functionalities 3: Navigation to Registration Page from Login Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.assertIn("Register", self.driver.title)
        self.driver.find_element(By.LINK_TEXT, 'Back to Login').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_recipe_submission(self):
        # Functionalities 4: Recipe Submission
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Recipe').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'title').send_keys('New Recipe')
        self.driver.find_element(By.NAME, 'ingredients').send_keys('Ingredient1, Ingredient2')
        self.driver.find_element(By.NAME, 'instructions').send_keys('Step 1, Step 2')
        self.driver.find_element(By.XPATH, '//button[text()="Submit Recipe"]').click()
        time.sleep(1)
        self.assertIn("Home", self.driver.title)

    def test_recipe_browsing(self):
        # Functionalities 5: Recipe Browsing
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'keyword').send_keys('Spaghetti')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)
        self.assertIn("Spaghetti", self.driver.page_source)

    def test_view_recipe_details(self):
        # Functionalities 6: View Recipe Details
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Spaghetti').click()
        time.sleep(1)
        self.assertIn("Spaghetti", self.driver.page_source)

    def test_navigation_from_recipe_browsing_to_home(self):
        # Functionalities 7: Navigation from Recipe Browsing to Home Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        time.sleep(1)
        self.assertIn("Home", self.driver.title)

    def test_user_profile_page(self):
        # Functionalities 8: User Profile Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)
        self.assertIn("User Profile", self.driver.title)

    def test_account_deletion(self):
        # Functionalities 9: Account Deletion
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[text()="Delete Account"]').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_navigation_from_recipe_details_to_home(self):
        # Functionalities 10: Navigation from Recipe Details to Home Page
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Spaghetti').click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Back to Browsing').click()
        time.sleep(1)
        self.assertIn("Browse Recipes", self.driver.title)

if __name__ == '__main__':
    unittest.main()
