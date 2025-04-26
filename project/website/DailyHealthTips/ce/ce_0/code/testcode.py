import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8151/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Today's Health Tip", self.driver.title)  # Verify redirection to tips page

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.assertIn("Register", self.driver.title)  # Verify redirection to registration page

    def test_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_current_daily_health_tip(self):
        # Functionalities 4: View Current Daily Health Tip
        self.login("admin", "admin123")
        tip_text = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertIn("Stay hydrated", tip_text)  # Check for the current tip

    def test_navigate_tips(self):
        # Functionalities 5: Navigate to Previous or Next Tips
        self.login("admin", "admin123")

        # Click on Next Tip (assuming button exists)
        self.driver.find_element(By.LINK_TEXT, 'Next Tip').click()
        next_tip_text = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertNotEqual(next_tip_text, "Stay hydrated")  # Ensure it's a different tip

        # Click on Previous Tip (assuming button exists)
        self.driver.find_element(By.LINK_TEXT, 'Previous Tip').click()
        previous_tip_text = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertEqual(previous_tip_text, "Stay hydrated")  # Ensure we return to the original tip

    def test_view_archive(self):
        # Functionalities 6: View Historical Daily Health Tips Archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        self.assertIn("Tips Archive", self.driver.title)  # Verify archive page title

    def test_submit_feedback(self):
        # Functionalities 8: Submit Feedback on Daily Health Tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Give Feedback').click()

        feedback_text = "This is a great tip!"
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify redirection back to tips page
        self.assertIn("Today's Health Tip", self.driver.title)

    def test_data_storage_retrieval(self):
        # Functionalities 9: Data Storage and Retrieval
        self.fail("Not implemented")  # Placeholder for future implementation

    def test_application_state_management(self):
        # Functionalities 10: Application State Management
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
