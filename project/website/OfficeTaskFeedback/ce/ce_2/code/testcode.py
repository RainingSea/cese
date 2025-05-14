import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import subprocess

class TestOfficeTaskFeedbackApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8102/login')
        time.sleep(1)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)

    def test_1_user_registration(self):
        """Test Functionality 1: User Registration"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.assertIn("Register", self.driver.title)

        # Test successful registration
        self.driver.find_element(By.NAME, 'username').send_keys("newuser")
        self.driver.find_element(By.NAME, 'password').send_keys("newpass123")
        self.driver.find_element(By.NAME, 'confirm_password').send_keys("newpass123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

        # Test registration with existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.NAME, 'confirm_password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertEqual(error_message, "Username already exists")

    def test_2_user_login(self):
        """Test Functionality 2: User Login"""
        # Test successful login
        self.login("employee1", "emp123")
        self.assertIn("My Feedback", self.driver.page_source)
        
        # Test invalid login
        self.driver.get('http://localhost:8102/login')
        self.login("wronguser", "wrongpass")
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertEqual(error_message, "Invalid credentials")

    def test_3_feedback_submission(self):
        """Test Functionality 3: Feedback Submission"""
        self.login("employee1", "emp123")
        
        # Navigate to feedback page
        self.driver.find_element(By.LINK_TEXT, 'Submit New Feedback').click()
        time.sleep(1)
        self.assertIn("Submit Feedback", self.driver.title)
        
        # Test successful submission
        self.driver.find_element(By.NAME, 'task').send_keys("New Task")
        self.driver.find_element(By.NAME, 'feedback').send_keys("This is test feedback")
        category_select = Select(self.driver.find_element(By.NAME, 'category'))
        category_select.select_by_visible_text("Task Clarity")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)
        self.assertIn("My Feedback", self.driver.page_source)
        
        # Test submission without required fields
        self.driver.find_element(By.LINK_TEXT, 'Submit New Feedback').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)
        # Check we're still on feedback page (form validation prevents submission)
        self.assertIn("Submit Feedback", self.driver.title)

    def test_4_feedback_categorization(self):
        """Test Functionality 4: Feedback Categorization"""
        self.login("employee1", "emp123")
        self.driver.find_element(By.LINK_TEXT, 'Submit New Feedback').click()
        time.sleep(1)
        
        # Test category selection
        category_select = Select(self.driver.find_element(By.NAME, 'category'))
        category_select.select_by_visible_text("Resources")
        selected_category = category_select.first_selected_option.text
        self.assertEqual(selected_category, "Resources")
        
        # Submit feedback and verify category
        self.driver.find_element(By.NAME, 'task').send_keys("Categorized Task")
        self.driver.find_element(By.NAME, 'feedback').send_keys("Testing categorization")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)
        self.assertIn("Resources", self.driver.page_source)

    def test_5_manager_review_feedback(self):
        """Test Functionality 5: Manager Review of Feedback"""
        self.login("admin", "admin123")
        self.assertIn("Feedback Dashboard", self.driver.title)
        
        # Check feedback list is displayed
        feedback_table = self.driver.find_element(By.TAG_NAME, 'table')
        rows = feedback_table.find_elements(By.TAG_NAME, 'tr')
        self.assertGreater(len(rows), 1)  # Header row + at least one feedback
        
        # Test category filtering
        category_select = Select(self.driver.find_element(By.NAME, 'category'))
        category_select.select_by_visible_text("Task Clarity")
        time.sleep(1)
        filtered_rows = self.driver.find_elements(By.XPATH, '//tbody/tr')
        for row in filtered_rows:
            category = row.find_elements(By.TAG_NAME, 'td')[4].text
            self.assertEqual(category, "Task Clarity")

    def test_6_view_feedback_status(self):
        """Test Functionality 6: View Feedback Status"""
        self.login("employee1", "emp123")
        
        # Check feedback status is displayed
        status_elements = self.driver.find_elements(By.XPATH, '//small[@class]')
        self.assertGreater(len(status_elements), 0)
        
        # Check status colors (visual verification would be manual)
        for element in status_elements:
            self.assertIn(element.text, ["Pending", "In Review", "Addressed"])

    def test_7_user_logout(self):
        """Test Functionality 7: User Logout"""
        self.login("employee1", "emp123")
        
        # Test logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)
        
        # Test access after logout
        self.driver.get('http://localhost:8102/employee_dashboard')
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_8_return_to_login_page(self):
        """Test Functionality 8: Return to Login Page"""
        # Test logout returns to login
        self.login("employee1", "emp123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)
        
        # Test register link from login page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
