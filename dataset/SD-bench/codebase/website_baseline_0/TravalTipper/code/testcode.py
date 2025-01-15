import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8558')

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

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message
        error_message = self.driver.find_element(By.XPATH, '//p[@style="color:red;"]').text
        self.assertEqual(error_message, "Username already exists.")

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8558')
        time.sleep(1)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to travel details page
        self.assertIn("Travel Details", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8558')
        self.login("invalid_user", "invalid_pass")

        # Verify redirection back to login page
        self.assertIn("Login", self.driver.title)

    def test_input_travel_details(self):
        # Login and navigate to the Travel Tips input section
        self.login("admin", "admin123")
        time.sleep(1)

        # Enter valid travel details and submit
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'duration').send_keys('5')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,culture')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Verify recommendations are displayed
        self.assertIn("Travel Recommendations", self.driver.title)

        # Submit the form with incomplete travel details
        self.driver.get('http://localhost:8558/travel_details')
        self.driver.find_element(By.NAME, 'destination').send_keys('')
        self.driver.find_element(By.NAME, 'duration').send_keys('')
        self.driver.find_element(By.NAME, 'interests').send_keys('')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Verify error message
        self.assertIn("Travel Details", self.driver.title)

    def test_view_recommendations(self):
        # Login and input travel details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'duration').send_keys('5')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,culture')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Verify recommendations are displayed
        self.assertIn("Travel Recommendations", self.driver.title)

        # Refresh the page and verify recommendations remain visible
        self.driver.refresh()
        time.sleep(1)
        self.assertIn("Travel Recommendations", self.driver.title)

    def test_search_for_tips(self):
        # This functionality is not implemented in the codebase
        self.fail("Search for Tips functionality not implemented")

    def test_save_favorite_travel_tips(self):
        # Login and input travel details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'duration').send_keys('5')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,culture')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Save a travel tip to favorites
        self.driver.find_element(By.XPATH, '//button[text()="Save to Favorites"]').click()
        time.sleep(1)

        # Navigate to the favorites section
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        time.sleep(1)

        # Verify the saved travel tips are displayed
        self.assertIn("Your Favorite Tips", self.driver.title)

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8558/travel_details')
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Login and input travel details
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'destination').send_keys('Paris')
        self.driver.find_element(By.NAME, 'duration').send_keys('5')
        self.driver.find_element(By.NAME, 'interests').send_keys('art,culture')
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        time.sleep(1)

        # Click the back button to return to the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Back').click()
        time.sleep(1)

        # Verify redirection to travel details page
        self.assertIn("Travel Details", self.driver.title)

    def test_view_saved_travel_tips(self):
        # Login and navigate to the favorites section
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        time.sleep(1)

        # Verify the user's saved travel tips are displayed
        self.assertIn("Your Favorite Tips", self.driver.title)

        # This functionality is not implemented in the codebase
        self.fail("View details of a saved travel tip functionality not implemented")

if __name__ == '__main__':
    unittest.main()
