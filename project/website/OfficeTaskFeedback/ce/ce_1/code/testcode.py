import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8100/login')
        time.sleep(1)  # Wait for page to load

    def tearDown(self):
        # Close the web driver session and stop the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Functionality 1: User Registration
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        
        # Verify registration page is displayed
        self.assertIn("Register", self.driver.title)
        
        # Test successful registration
        username = "test_user_" + str(int(time.time()))
        password = "test123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)
        
        # Test registration with existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Register", self.driver.title)
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertIn("Registration failed", error_message)

    def test_user_login(self):
        # Functionality 2: User Login
        # Verify login page is displayed
        self.assertIn("Login", self.driver.title)
        
        # Test successful login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        
        # Logout and test invalid credentials
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.login("invalid", "invalid")
        time.sleep(1)
        self.assertIn("Login", self.driver.title)
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertIn("Invalid credentials", error_message)

    def test_feedback_submission(self):
        # Functionality 3: Feedback Submission
        self.login("employee1", "employee123")
        
        # Verify feedback form is displayed
        form = self.driver.find_element(By.XPATH, '//form[@action="/submit_feedback"]')
        self.assertTrue(form.is_displayed())
        
        # Test successful feedback submission
        category_select = Select(self.driver.find_element(By.NAME, 'category'))
        category_select.select_by_visible_text("Technical")
        self.driver.find_element(By.NAME, 'content').send_keys("Test feedback content")
        self.driver.find_element(By.XPATH, '//form[@action="/submit_feedback"]/button').click()
        time.sleep(1)
        
        # Verify feedback appears in the list
        feedback_table = self.driver.find_element(By.XPATH, '//div[@class="employee-view"]/table')
        self.assertIn("Test feedback content", feedback_table.text)
        
        # Test submission without required fields
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.XPATH, '//form[@action="/submit_feedback"]/button').click()
        time.sleep(1)
        # Should stay on same page with error (though UI doesn't show it currently)
        self.assertIn("Dashboard", self.driver.title)

    def test_feedback_categorization(self):
        # Functionality 4: Feedback Categorization
        self.login("employee1", "employee123")
        
        # Verify categories dropdown
        category_select = Select(self.driver.find_element(By.NAME, 'category'))
        categories = [option.text for option in category_select.options]
        expected_categories = ["General", "Technical", "HR", "Other"]
        self.assertEqual(categories, expected_categories)
        
        # Test category selection and submission
        test_category = "HR"
        category_select.select_by_visible_text(test_category)
        self.driver.find_element(By.NAME, 'content').send_keys("Categorized feedback test")
        self.driver.find_element(By.XPATH, '//form[@action="/submit_feedback"]/button').click()
        time.sleep(1)
        
        # Verify category is correctly stored and displayed
        feedback_table = self.driver.find_element(By.XPATH, '//div[@class="employee-view"]/table')
        self.assertIn(test_category, feedback_table.text)

    def test_manager_review(self):
        # Functionality 5: Manager Review of Feedback
        self.login("manager_john", "manager123")
        
        # Verify manager view is displayed
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'manager-view').is_displayed())
        
        # Verify feedback list is displayed
        feedback_table = self.driver.find_element(By.XPATH, '//div[@class="manager-view"]/table')
        self.assertTrue(feedback_table.is_displayed())
        
        # Verify feedback details are present
        rows = feedback_table.find_elements(By.TAG_NAME, 'tr')
        self.assertGreater(len(rows), 1)  # Header row + at least one feedback
        
        # Test status update functionality
        status_select = Select(feedback_table.find_element(By.NAME, 'status'))
        status_select.select_by_visible_text("In Review")
        feedback_table.find_element(By.XPATH, './/button[text()="Update"]').click()
        time.sleep(1)
        
        # Verify status was updated (would need more specific selectors in real test)
        updated_rows = feedback_table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn("In Review", updated_rows[1].text)

    def test_view_feedback_status(self):
        # Functionality 6: View Feedback Status
        self.login("employee1", "employee123")
        
        # Verify feedback status table is displayed
        feedback_table = self.driver.find_element(By.XPATH, '//div[@class="employee-view"]/table')
        self.assertTrue(feedback_table.is_displayed())
        
        # Check if status column exists
        headers = [th.text for th in feedback_table.find_elements(By.TAG_NAME, 'th')]
        self.assertIn("Status", headers)
        
        # Logout and login as manager to update status
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.login("manager_john", "manager123")
        
        # Update status of first feedback
        feedback_table = self.driver.find_element(By.XPATH, '//div[@class="manager-view"]/table')
        status_select = Select(feedback_table.find_element(By.NAME, 'status'))
        status_select.select_by_visible_text("Addressed")
        feedback_table.find_element(By.XPATH, './/button[text()="Update"]').click()
        time.sleep(1)
        
        # Logout and login as employee to check updated status
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.login("employee1", "employee123")
        
        # Verify status was updated
        updated_table = self.driver.find_element(By.XPATH, '//div[@class="employee-view"]/table')
        self.assertIn("Addressed", updated_table.text)

    def test_user_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        
        # Verify dashboard is displayed
        self.assertIn("Dashboard", self.driver.title)
        
        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        
        # Verify redirected to login page
        self.assertIn("Login", self.driver.title)
        
        # Attempt to access dashboard directly
        self.driver.get('http://localhost:8100/dashboard')
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_return_to_login_page(self):
        # Functionality 8: Return to Login Page
        self.login("admin", "admin123")
        
        # Logout from dashboard
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)
        
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
