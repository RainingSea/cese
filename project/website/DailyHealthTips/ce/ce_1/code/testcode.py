import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8316/')  # Accessing the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
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
        self.assertIn("Today's Health Tip", self.driver.title)  # Check if redirected to tips page

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.assertIn("Register", self.driver.title)  # Verify that the Registration Page has loaded

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
        self.assertIn("Today's Health Tip", self.driver.page_source)  # Check if the tip is displayed

    def test_navigate_to_archive(self):
        # Functionalities 6: View Historical Daily Health Tips Archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        self.assertIn("Archive of Health Tips", self.driver.title)  # Check if the archive page is displayed

    def test_submit_feedback(self):
        # Functionalities 8: Submit Feedback on Daily Health Tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Give Feedback').click()

        feedback_text = "Great tips! I found them very helpful."
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that the feedback submission is successful
        self.assertIn("Today's Health Tip", self.driver.title)  # Check if redirected back to tips page

if __name__ == '__main__':
    unittest.main()
