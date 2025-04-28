import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8436/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8436/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.get('http://localhost:8436/register')
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already exists", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials

        # Verify redirection to travel details page
        self.assertIn("Travel Details", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8436/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_input_travel_details(self):
        # Functionality 3: Input Travel Details
        self.login("admin", "admin123")  # Login first

        # Verify travel details input form is displayed
        self.assertIn("Travel Details", self.driver.title)

        # Enter valid travel details
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'duration').send_keys("5 days")
        self.driver.find_element(By.NAME, 'interests').click()  # Select an interest
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify that tips are generated
        self.assertIn("Tip for Paris", self.driver.page_source)

        # Attempt to submit with incomplete details
        self.driver.find_element(By.NAME, 'destination').clear()  # Clear destination
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_recommendations(self):
        # Functionality 4: View Recommendations
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.NAME, 'destination').send_keys("Bali")
        self.driver.find_element(By.NAME, 'duration').send_keys("7 days")
        self.driver.find_element(By.NAME, 'interests').click()  # Select an interest
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify recommendations are displayed
        self.assertIn("Tip for Bali", self.driver.page_source)

        # Refresh the page and verify recommendations remain
        self.driver.refresh()
        self.assertIn("Tip for Bali", self.driver.page_source)

    def test_search_for_tips(self):
        # Functionality 5: Search for Tips
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.NAME, 'destination').send_keys("Eiffel Tower")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify relevant tips are displayed
        self.assertIn("Tip for Eiffel Tower", self.driver.page_source)

        # Search for a non-existent tip
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.NAME, 'destination').send_keys("Nonexistent Place")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.assertIn("No tips found", self.driver.page_source)

    def test_save_favorite_tips(self):
        # Functionality 6: Save Favorite Travel Tips
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.NAME, 'destination').send_keys("Bali")
        self.driver.find_element(By.NAME, 'duration').send_keys("7 days")
        self.driver.find_element(By.NAME, 'interests').click()  # Select an interest
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Save a tip (assuming there's a save button next to tips)
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()  # Simulating save action
        self.assertIn("Tip saved", self.driver.page_source)

        # Attempt to save the same tip again
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()  # Simulating save action again
        self.assertIn("Tip is already saved", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8436/travel_details')  # Navigate to travel details
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()  # Assuming there's a back button

        # Verify redirection back to dashboard
        self.assertIn("Travel Details", self.driver.title)

    def test_view_saved_travel_tips(self):
        # Functionality 9: View Saved Travel Tips
        self.login("admin", "admin123")  # Login first
        self.driver.get('http://localhost:8436/favorites')  # Navigate to favorites section

        # Verify saved travel tips are displayed
        self.assertIn("Your Saved Tips", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
