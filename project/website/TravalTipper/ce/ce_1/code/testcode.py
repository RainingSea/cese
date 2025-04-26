import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestTravelTipperApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8263/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the web application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the user is redirected to the travel details page
        self.assertIn("Travel Details", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8263/')  # Go back to login page
        self.login("admin", "wrongpassword")  # Invalid password

        # Verify error message for incorrect credentials
        self.assertIn("Login credentials are incorrect", self.driver.page_source)

    def test_input_travel_details(self):
        # Functionality 3: Input Travel Details
        self.login("admin", "admin123")
        
        # Verify that the travel details input form is displayed
        self.assertIn("Enter Travel Details", self.driver.title)

        # Input valid travel details
        self.driver.find_element(By.NAME, 'destination').send_keys("Paris")
        self.driver.find_element(By.NAME, 'interests').send_keys("sightseeing")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify that recommendations are displayed
        self.assertIn("Travel Tips", self.driver.page_source)

        # Submit with incomplete details
        self.driver.get('http://localhost:8263/travel')  # Go back to travel details page
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify error message for incomplete details
        self.assertIn("All fields are required", self.driver.page_source)

    def test_view_recommendations(self):
        # Functionality 4: View Recommendations
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'destination').send_keys("Bali")
        self.driver.find_element(By.NAME, 'interests').send_keys("beaches")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify recommendations are displayed
        self.assertIn("Travel Tips", self.driver.page_source)

        # Refresh the page and check if recommendations remain visible
        self.driver.refresh()
        self.assertIn("Travel Tips", self.driver.page_source)

    def test_search_tips(self):
        # Functionality 5: Search for Tips
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8263/travel')  # Navigate to travel details page

        # Input travel details and get tips
        self.driver.find_element(By.NAME, 'destination').send_keys("Bangkok")
        self.driver.find_element(By.NAME, 'interests').send_keys("food")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify relevant tips are displayed
        self.assertIn("street food", self.driver.page_source)

        # Search for a non-existent tip
        self.driver.get('http://localhost:8263/travel')  # Go back to travel details page
        self.driver.find_element(By.NAME, 'destination').send_keys("Nowhere")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Verify no tips found message
        self.assertIn("No tips found", self.driver.page_source)

    def test_save_favorite_tips(self):
        # Functionality 6: Save Favorite Travel Tips
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8263/travel')  # Navigate to travel details page

        # Input travel details and get tips
        self.driver.find_element(By.NAME, 'destination').send_keys("Grand Canyon")
        self.driver.find_element(By.NAME, 'interests').send_keys("hiking")
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()

        # Save a tip
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()  # Assuming there's a save button next to tips

        # Verify confirmation message
        self.assertIn("Tip saved to favorites", self.driver.page_source)

        # Attempt to save the same tip again
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Verify error message for already saved tip
        self.assertIn("Tip already saved", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the travel details page after logging out
        self.driver.get('http://localhost:8263/travel')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8263/travel')  # Navigate to travel details page

        # Click the back button
        self.driver.find_element(By.LINK_TEXT, 'Back to Travel Details').click()

        # Verify that the user is redirected back to the Dashboard Page
        self.assertIn("Enter Travel Details", self.driver.title)

    def test_view_saved_travel_tips(self):
        # Functionality 9: View Saved Travel Tips
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8263/favorites')  # Assuming there's a favorites page

        # Verify that saved travel tips are displayed
        self.assertIn("Your Favorite Tips", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
