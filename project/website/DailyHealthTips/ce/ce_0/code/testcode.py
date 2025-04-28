import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8315/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Today's Health Tip", self.driver.title)  # Check if redirected to tips page

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)  # Check if redirected to registration page

    def test_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_current_daily_health_tip(self):
        # Functionalities 4: View Current Daily Health Tip
        self.login("admin", "admin123")
        self.assertIn("Today's Health Tip", self.driver.page_source)  # Check if the tip is displayed

    def test_navigate_tips(self):
        # Functionalities 5: Navigate to Previous or Next Tips
        self.login("admin", "admin123")
        
        # Click on Next Tip
        self.driver.find_element(By.LINK_TEXT, 'Next Tip').click()
        self.assertIn("Today's Health Tip", self.driver.page_source)  # Check if the next tip is displayed

        # Click on Previous Tip
        self.driver.find_element(By.LINK_TEXT, 'Previous Tip').click()
        self.assertIn("Today's Health Tip", self.driver.page_source)  # Check if the previous tip is displayed

    def test_view_archive(self):
        # Functionalities 6: View Historical Daily Health Tips Archive
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        self.assertIn("Archive of Health Tips", self.driver.title)  # Check if the archive page is displayed

    def test_search_tips(self):
        # Functionalities 7: Search for Specific Tips from the Tips Archive
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, 'search').send_keys("water")  # Assuming there's a search input
        self.driver.find_element(By.XPATH, '//input[@value="Search"]').click()
        self.assertIn("Drink plenty of water every day.", self.driver.page_source)  # Check if the search result is displayed

    def test_submit_feedback(self):
        # Functionalities 8: Submit Feedback on Daily Health Tips
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        feedback_text = "Great tips! Looking forward to more."
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//input[@value="Submit Feedback"]').click()
        self.assertIn("Today's Health Tip", self.driver.page_source)  # Check if redirected back to tips page

    def test_data_storage_retrieval(self):
        # Functionalities 9: Data Storage and Retrieval
        self.fail("Not implemented")  # Placeholder for future implementation

    def test_application_state_management(self):
        # Functionalities 10: Application State Management
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)  # Check if redirected to login page

if __name__ == '__main__':
    unittest.main()
