import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8098/')
        time.sleep(2)  # Wait for the application to start

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def logout(self):
        # Helper method to perform logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

    # Functionality 1: User Registration
    def test_user_registration(self):
        # Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.assertIn("Register", self.driver.title)

        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

        # Test registration with existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("manager")
        self.driver.find_element(By.NAME, 'password').send_keys("anypassword")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color: red;"]').text
        self.assertEqual(error_message, "Username already exists")

    # Functionality 2: User Login
    def test_user_login(self):
        # Test successful login
        self.login("manager", "manager123")
        self.assertIn("Dashboard", self.driver.title)
        self.logout()

        # Test invalid credentials
        self.login("invalid", "invalid")
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color: red;"]').text
        self.assertEqual(error_message, "Invalid credentials")

    # Functionality 3: Feedback Submission
    def test_feedback_submission(self):
        self.login("employee1", "employee123")
        
        # Test successful feedback submission
        category_select = Select(self.driver.find_element(By.ID, 'category'))
        category_select.select_by_visible_text("General")
        self.driver.find_element(By.ID, 'content').send_keys("This is a test feedback")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)
        
        # Verify feedback appears in the table
        feedback_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIn("This is a test feedback", feedback_table.text)
        
        # Test submitting without required fields
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)
        # The page should still be on dashboard with the form showing errors
        self.assertIn("Dashboard", self.driver.title)

    # Functionality 4: Feedback Categorization
    def test_feedback_categorization(self):
        self.login("employee1", "employee123")
        
        # Test category selection
        category_select = Select(self.driver.find_element(By.ID, 'category'))
        categories = [option.text for option in category_select.options]
        expected_categories = ["General", "Bug", "Feature Request", "Improvement", "Other"]
        self.assertEqual(categories, expected_categories)
        
        # Select a category and submit
        category_select.select_by_visible_text("Bug")
        self.driver.find_element(By.ID, 'content').send_keys("Bug report test")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)
        
        # Verify the category appears in the table
        feedback_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIn("Bug", feedback_table.text)

    # Functionality 5: Manager Review of Feedback
    def test_manager_review(self):
        self.login("manager", "manager123")
        
        # Check if manager sees all feedback
        feedback_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIn("employee1", feedback_table.text)
        
        # Check status update functionality
        status_select = Select(self.driver.find_element(By.NAME, 'status'))
        status_select.select_by_visible_text("approved")
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()
        time.sleep(1)
        
        # Verify status was updated
        updated_status = self.driver.find_element(By.XPATH, '//td[text()="approved"]')
        self.assertIsNotNone(updated_status)

    # Functionality 6: View Feedback Status
    def test_view_feedback_status(self):
        self.login("employee1", "employee123")
        
        # Check if feedback status is displayed
        feedback_table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIn("pending", feedback_table.text)
        
        # Login as manager and update status
        self.logout()
        self.login("manager", "manager123")
        status_select = Select(self.driver.find_element(By.NAME, 'status'))
        status_select.select_by_visible_text("approved")
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()
        time.sleep(1)
        self.logout()
        
        # Login as employee and check updated status
        self.login("employee1", "employee123")
        updated_status = self.driver.find_element(By.XPATH, '//td[text()="approved"]')
        self.assertIsNotNone(updated_status)

    # Functionality 7: User Logout
    def test_user_logout(self):
        self.login("employee1", "employee123")
        self.logout()
        self.assertIn("Login", self.driver.title)
        
        # Try to access dashboard after logout
        self.driver.get('http://localhost:8098/dashboard')
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    # Functionality 8: Return to Login Page
    def test_return_to_login(self):
        self.login("employee1", "employee123")
        self.logout()
        self.assertIn("Login", self.driver.title)
        
        # Test register link from login page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
