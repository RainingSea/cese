import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and the application
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
        self.assertIn("Daily Health Tip", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)

    def test_view_current_tip(self):
        # Functionalities 4: View Current Daily Health Tip
        self.login("admin", "admin123")
        current_tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertNotEqual(current_tip, "No tips available.")

    def test_navigate_tips(self):
        # Functionalities 5: Navigate to Previous or Next Tips
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Next Tip"]').click()
        next_tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertNotEqual(next_tip, "No next tip available.")
        
        self.driver.find_element(By.XPATH, '//button[text()="Previous Tip"]').click()
        previous_tip = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertNotEqual(previous_tip, "No previous tip available.")

    def test_view_tips_archive(self):
        # Functionalities 6: View Historical Daily Health Tips Archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        self.assertIn("Tips Archive", self.driver.title)

    def test_submit_feedback(self):
        # Functionalities 8: Submit Feedback on Daily Health Tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        feedback_text = "Great tips! I really appreciate them."
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        self.assertIn("Feedback", self.driver.title)

    def test_search_tips(self):
        # Functionalities 7: Search for Specific Tips from the Tips Archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        search_query = "hydrated"
        self.driver.find_element(By.NAME, 'search').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(results), 0)

if __name__ == '__main__':
    unittest.main()
