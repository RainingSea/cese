import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestSocialLearnApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8049/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains("Dashboard"))

    def logout(self):
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains("Login"))

    # Functionality 1: User Registration
    def test_user_registration(self):
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains("Register"))
        
        # Test successful registration
        self.driver.find_element(By.NAME, 'username').send_keys("testuser")
        self.driver.find_element(By.NAME, 'password').send_keys("testpass")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.title_contains("Login"))
        
        # Test duplicate username registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains("Register"))
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color: red;"]').text
        self.assertEqual(error_message, "Username already exists")

    # Functionality 2: User Login
    def test_user_login(self):
        # Test successful login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        self.logout()
        
        # Test invalid login
        self.driver.find_element(By.NAME, 'username').send_keys("wronguser")
        self.driver.find_element(By.NAME, 'password').send_keys("wrongpass")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color: red;"]').text
        self.assertEqual(error_message, "Invalid credentials")

    # Functionality 3: User Profile Management
    def test_profile_management(self):
        self.login("user1", "user123")
        
        # Navigate to profile page
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.title_contains("Profile"))
        
        # Test profile update
        textarea = self.driver.find_element(By.NAME, 'interests')
        textarea.clear()
        textarea.send_keys("mathematics,physics,chemistry")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        self.wait.until(EC.title_contains("Dashboard"))
        
        # Verify update
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.title_contains("Profile"))
        textarea = self.driver.find_element(By.NAME, 'interests')
        self.assertIn("chemistry", textarea.get_attribute("value"))

    # Functionality 4: Join Study Groups
    def test_join_study_groups(self):
        self.login("user1", "user123")
        
        # Navigate to groups page
        self.driver.find_element(By.LINK_TEXT, 'Groups').click()
        self.wait.until(EC.title_contains("Groups"))
        
        # Test joining a new group
        group_input = self.driver.find_element(By.NAME, 'group_name')
        group_input.send_keys("New Study Group")
        self.driver.find_element(By.XPATH, '//button[text()="Join"]').click()
        
        # Verify the group appears in the list
        groups_list = self.driver.find_elements(By.TAG_NAME, 'li')
        group_names = [group.text for group in groups_list]
        self.assertTrue(any("New Study Group" in name for name in group_names))

    # Functionality 5: Share and Access Educational Resources
    def test_educational_resources(self):
        self.login("admin", "admin123")
        
        # Navigate to resources page
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.wait.until(EC.title_contains("Resources"))
        
        # Test sharing a new resource
        self.driver.find_element(By.NAME, 'title').send_keys("New Resource")
        self.driver.find_element(By.NAME, 'type').send_keys("Article")
        self.driver.find_element(By.NAME, 'link').send_keys("https://example.com/new")
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()
        
        # Verify the resource appears in the list
        resources_list = self.driver.find_elements(By.TAG_NAME, 'li')
        resource_titles = [resource.text for resource in resources_list]
        self.assertTrue(any("New Resource" in title for title in resource_titles))

    # Functionality 6: Messaging in Study Groups
    def test_messaging(self):
        self.login("user1", "user123")
        
        # Navigate to messages page
        self.driver.find_element(By.LINK_TEXT, 'Messages').click()
        self.wait.until(EC.title_contains("Messages"))
        
        # Test sending a message
        self.driver.find_element(By.NAME, 'receiver').send_keys("admin")
        self.driver.find_element(By.NAME, 'content').send_keys("Test message")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        
        # Verify the message appears in the list
        messages = self.driver.find_elements(By.TAG_NAME, 'li')
        message_contents = [message.text for message in messages]
        self.assertTrue(any("Test message" in content for content in message_contents))

    # Functionality 7: User Logout
    def test_logout(self):
        self.login("admin", "admin123")
        self.logout()
        
        # Try to access dashboard after logout
        self.driver.get('http://localhost:8049/dashboard')
        self.wait.until(EC.title_contains("Login"))

    # Functionality 8: Navigate Back to Dashboard
    def test_navigate_back_to_dashboard(self):
        self.login("user1", "user123")
        
        # Go to profile page then back to dashboard
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.title_contains("Profile"))
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        self.wait.until(EC.title_contains("Dashboard"))

    # Functionality 9: View Educational Resource Details
    def test_view_resource_details(self):
        self.login("admin", "admin123")
        
        # Navigate to resources page
        self.driver.find_element(By.LINK_TEXT, 'Resources').click()
        self.wait.until(EC.title_contains("Resources"))
        
        # Verify resource details are displayed
        resources = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertTrue(len(resources) > 0)
        for resource in resources:
            self.assertTrue(resource.text.strip() != "")

if __name__ == '__main__':
    unittest.main()
