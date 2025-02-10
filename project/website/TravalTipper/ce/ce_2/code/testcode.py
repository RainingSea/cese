import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8661/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to Dashboard Page
        self.assertIn("Travel Details", self.driver.page_source)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8661/')
        self.login("invalid_user", "invalid_pass")

        # Verify error message for incorrect credentials
        self.assertIn("Login", self.driver.title)

    def test_input_travel_details(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify the Travel Tips input form is displayed
        self.assertIn("Enter Travel Details", self.driver.page_source)

        # Enter valid travel details and submit
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,culture')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Verify personalized travel tips are displayed
        self.assertIn("Your Travel Tips", self.driver.page_source)

        # Submit the form with incomplete travel details
        self.driver.get('http://localhost:8661/travel_details')
        self.driver.find_element(By.NAME, 'destination').send_keys('')
        self.driver.find_element(By.NAME, 'interests').send_keys('')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Verify error message for incomplete details
        self.assertIn("Enter Travel Details", self.driver.page_source)

    def test_view_recommendations(self):
        # Login and input travel details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,culture')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Verify recommendations are displayed
        self.assertIn("Your Travel Tips", self.driver.page_source)

        # Refresh the page and verify recommendations remain visible
        self.driver.refresh()
        self.assertIn("Your Travel Tips", self.driver.page_source)

    def test_search_for_tips(self):
        # Functionality not implemented in the codebase
        self.fail("Search for Tips functionality not implemented")

    def test_save_favorite_travel_tips(self):
        # Functionality not implemented in the codebase
        self.fail("Save Favorite Travel Tips functionality not implemented")

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Logout from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8661/travel_details')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Login and input travel details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,culture')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()

        # Click the back button to return to the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Back to Travel Details').click()

        # Verify redirection back to the Dashboard Page
        self.assertIn("Enter Travel Details", self.driver.page_source)

    def test_view_saved_travel_tips(self):
        # Functionality not implemented in the codebase
        self.fail("View Saved Travel Tips functionality not implemented")

if __name__ == '__main__':
    unittest.main()
