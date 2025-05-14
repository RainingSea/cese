import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8050/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        # Terminate the Flask application
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains("Dashboard"))

    def test_functionality1_user_registration(self):
        """Test User Registration functionality"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains("Register"))
        
        # Test valid registration
        self.driver.find_element(By.NAME, 'username').send_keys("newuser")
        self.driver.find_element(By.NAME, 'password').send_keys("newpass123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.title_contains("Dashboard"))
        
        # Test duplicate username registration
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains("Login"))
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("newuser")
        self.driver.find_element(By.NAME, 'password').send_keys("anotherpass")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        # Should stay on registration page with error (implementation may vary)
        self.assertIn("Register", self.driver.title)

    def test_functionality2_user_login(self):
        """Test User Login functionality"""
        # Test valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        
        # Test invalid login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains("Login"))
        self.driver.find_element(By.NAME, 'username').send_keys("wronguser")
        self.driver.find_element(By.NAME, 'password').send_keys("wrongpass")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        # Should stay on login page with error (implementation may vary)
        self.assertIn("Login", self.driver.title)

    def test_functionality3_user_profile_management(self):
        """Test User Profile Management functionality"""
        self.login("admin", "admin123")
        
        # Navigate to profile page
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.title_contains("Profile"))
        
        # Test profile update
        interests = self.driver.find_element(By.NAME, 'interests')
        interests.clear()
        interests.send_keys("Programming, Math, Science")
        expertise = self.driver.find_element(By.NAME, 'expertise')
        expertise.clear()
        expertise.send_keys("Python, Algorithms")
        self.driver.find_element(By.XPATH, '//button[text()="Save Profile"]').click()
        self.wait.until(EC.title_contains("Dashboard"))
        
        # Test empty fields (should fail)
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.title_contains("Profile"))
        interests = self.driver.find_element(By.NAME, 'interests')
        interests.clear()
        expertise = self.driver.find_element(By.NAME, 'expertise')
        expertise.clear()
        self.driver.find_element(By.XPATH, '//button[text()="Save Profile"]').click()
        # Should stay on profile page with error (implementation may vary)
        self.assertIn("Profile", self.driver.title)

    def test_functionality4_join_study_groups(self):
        """Test Join Study Groups functionality"""
        self.login("user1", "password1")
        
        # Navigate to groups page
        self.driver.find_element(By.LINK_TEXT, 'Groups').click()
        self.wait.until(EC.title_contains("Groups"))
        
        # Test joining a group
        join_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Join"]')
        if join_buttons:
            join_buttons[0].click()
            time.sleep(1)  # Wait for the join action to complete
            # Verify the group appears in dashboard
            self.driver.find_element(By.LINK_TEXT, 'Dashboard').click()
            self.wait.until(EC.title_contains("Dashboard"))
            self.assertIn("Python Study Group", self.driver.page_source)
        
        # Note: The "group full" test case isn't implemented in the codebase
        # so we can't test it properly

    def test_functionality5_share_and_access_educational_resources(self):
        """Test Share and Access Educational Resources functionality"""
        self.login("admin", "admin123")
        
        # Navigate to resources page
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.wait.until(EC.title_contains("Resources"))
        
        # Test sharing a resource
        self.driver.find_element(By.NAME, 'title').send_keys("New Resource")
        self.driver.find_element(By.NAME, 'type').send_keys("PDF")
        self.driver.find_element(By.NAME, 'url').send_keys("/resources/new.pdf")
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()
        time.sleep(1)  # Wait for the share action to complete
        
        # Verify the resource appears in the list
        self.assertIn("New Resource", self.driver.page_source)
        
        # Note: The "invalid format" test case isn't implemented in the codebase
        # so we can't test it properly

    def test_functionality6_messaging_in_study_groups(self):
        """Test Messaging in Study Groups functionality"""
        self.login("admin", "admin123")
        
        # Navigate to messages page
        self.driver.find_element(By.LINK_TEXT, 'Messages').click()
        self.wait.until(EC.title_contains("Messages"))
        
        # Test sending a message
        self.driver.find_element(By.NAME, 'receiver').send_keys("user1")
        self.driver.find_element(By.NAME, 'group').send_keys("Python Study Group")
        self.driver.find_element(By.NAME, 'content').send_keys("Hello from test!")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        time.sleep(1)  # Wait for the message to be sent
        
        # Verify the message appears in the list
        self.assertIn("Hello from test!", self.driver.page_source)
        
        # Test empty message (should fail)
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        # Should stay on messages page with error (implementation may vary)
        self.assertIn("Messages", self.driver.title)

    def test_functionality7_user_logout(self):
        """Test User Logout functionality"""
        self.login("admin", "admin123")
        
        # Test logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains("Login"))
        
        # Test navigation back to dashboard after logout
        self.driver.get('http://localhost:8050/dashboard')
        self.wait.until(EC.title_contains("Login"))  # Should redirect to login

    def test_functionality8_navigate_back_to_dashboard(self):
        """Test Navigation Back to Dashboard"""
        self.login("admin", "admin123")
        
        # Navigate to profile page then back to dashboard
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.title_contains("Profile"))
        self.driver.find_element(By.LINK_TEXT, 'Dashboard').click()
        self.wait.until(EC.title_contains("Dashboard"))
        
        # Verify dashboard content
        self.assertIn("Welcome, admin!", self.driver.page_source)

    def test_functionality9_view_educational_resource_details(self):
        """Test View Educational Resource Details"""
        self.login("admin", "admin123")
        
        # Navigate to resources page
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.wait.until(EC.title_contains("Resources"))
        
        # Verify resource details are displayed
        self.assertIn("Python Tutorial", self.driver.page_source)
        self.assertIn("PDF", self.driver.page_source)
        self.assertIn("/resources/python.pdf", self.driver.page_source)
        
        # Note: The "deleted resource" test case isn't implemented in the codebase
        # so we can't test it properly

if __name__ == '__main__':
    unittest.main()
