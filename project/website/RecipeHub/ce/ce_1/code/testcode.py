import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestRecipeHubApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8403/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Verify redirection to Home Page

    def test_user_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)  # Verify redirection to Login Page

    def test_navigate_to_registration(self):
        # Functionalities 3: Navigation to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)  # Verify Registration Page loaded
        self.driver.back()  # Navigate back to Login Page
        self.assertIn("Login", self.driver.title)  # Verify back to Login Page

    def test_recipe_submission(self):
        # Functionalities 4: Recipe Submission
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Recipe').click()
        self.driver.find_element(By.NAME, 'title').send_keys("New Recipe")
        self.driver.find_element(By.NAME, 'ingredients').send_keys("Ingredient1, Ingredient2")
        self.driver.find_element(By.NAME, 'instructions').send_keys("Instructions for the recipe.")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        self.assertIn("Recipe submitted successfully!", self.driver.page_source)  # Verify success message

    def test_browse_recipes(self):
        # Functionalities 5: Recipe Browsing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.assertIn("Browse Recipes", self.driver.title)  # Verify Browsing Page loaded

    def test_view_recipe_details(self):
        # Functionalities 6: View Recipe Details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()  # Assuming 'Pasta' is in the list
        self.assertIn("Recipe Details", self.driver.title)  # Verify Recipe Details Page loaded

    def test_navigation_from_browsing_to_home(self):
        # Functionalities 7: Navigation from Recipe Browsing to Home Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        self.assertIn("Home", self.driver.title)  # Verify redirection to Home Page

    def test_user_profile_page(self):
        # Functionalities 8: User Profile Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'User Profile').click()
        self.assertIn("User Profile", self.driver.title)  # Verify User Profile Page loaded

    def test_navigation_from_recipe_details_to_home(self):
        # Functionalities 10: Navigation from Recipe Details to Home Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Browse Recipes').click()
        self.driver.find_element(By.LINK_TEXT, 'Pasta').click()  # Assuming 'Pasta' is in the list
        self.driver.find_element(By.LINK_TEXT, 'Back to Home').click()
        self.assertIn("Home", self.driver.title)  # Verify redirection to Home Page

if __name__ == '__main__':
    unittest.main()
