import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8660/') 

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration Page is displayed
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.ID, 'username').send_keys("admin")
        self.driver.find_element(By.ID, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Registration", self.driver.title)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and the user is redirected to the Dashboard Page
        self.assertIn("Travel Tips", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8660/')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_input_travel_details(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify the Travel Tips input form is displayed
        self.assertIn("Travel Tips", self.driver.title)

        # Enter valid travel details and submit
        self.driver.find_element(By.ID, 'destination').send_keys("Paris")
        self.driver.find_element(By.XPATH, '//input[@value="Get Tips"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify personalized travel tips are generated
        self.assertIn("Your Recommendations", self.driver.page_source)

        # Submit the form with incomplete travel details
        self.driver.find_element(By.ID, 'destination').clear()
        self.driver.find_element(By.XPATH, '//input[@value="Get Tips"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Travel Tips", self.driver.title)

    def test_view_recommendations(self):
        # Login successfully
        self.login("admin", "admin123")

        # Enter valid travel details and submit
        self.driver.find_element(By.ID, 'destination').send_keys("Paris")
        self.driver.find_element(By.XPATH, '//input[@value="Get Tips"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify recommendations are displayed
        self.assertIn("Your Recommendations", self.driver.page_source)

        # Refresh the page
        self.driver.refresh()
        time.sleep(1)  # Wait for the page to reload

        # Verify the recommendations remain visible
        self.assertIn("Your Recommendations", self.driver.page_source)

    def test_search_for_tips(self):
        # This functionality is not implemented in the codebase
        self.fail("Search for Tips functionality not implemented")

    def test_save_favorite_travel_tips(self):
        # This functionality is not implemented in the codebase
        self.fail("Save Favorite Travel Tips functionality not implemented")

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8660/travel_tips')
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected back to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # This functionality is not implemented in the codebase
        self.fail("Navigate Back to Dashboard functionality not implemented")

    def test_view_saved_travel_tips(self):
        # This functionality is not implemented in the codebase
        self.fail("View Saved Travel Tips functionality not implemented")

if __name__ == '__main__':
    unittest.main()
