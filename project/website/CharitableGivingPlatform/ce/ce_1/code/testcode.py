import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestCharitableGivingPlatform(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8565/')
        time.sleep(1)  # Wait for the page to load

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

    def test_login(self):
        """Functionalities 1: User Login"""
        # Test with valid credentials
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        
        # Test with invalid credentials
        self.driver.get('http://localhost:8565/')
        self.login("invalid", "invalid")
        error_message = self.driver.find_element(By.XPATH, '//p[@style="color:red"]')
        self.assertEqual(error_message.text, "Invalid credentials")

    def test_navigate_to_registration_page(self):
        """Functionalities 2: Navigate to Registration Page"""
        register_link = self.driver.find_element(By.LINK_TEXT, 'Register')
        register_link.click()
        time.sleep(1)
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        """Functionalities 3: User Registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        
        # Test successful registration
        username = "test_user_" + str(int(time.time()))
        password = "test_password"
        
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        # Should be redirected to dashboard after successful registration
        self.assertIn("Dashboard", self.driver.title)
        
        # Test registration with existing username
        self.driver.get('http://localhost:8565/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("anypassword")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        
        error_message = self.driver.find_element(By.XPATH, '//p[@style="color:red"]')
        self.assertEqual(error_message.text, "Username already exists")

    def test_view_charities_on_dashboard(self):
        """Functionalities 4: View Charities on the Dashboard Page"""
        self.login("admin", "admin123")
        
        # Check if charities are displayed
        charities = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertGreater(len(charities), 0)
        
        # Check if charity details are present
        charity_names = [c.text for c in charities]
        self.assertIn("Save the Children", " ".join(charity_names))
        self.assertIn("Red Cross", " ".join(charity_names))
        self.assertIn("WWF", " ".join(charity_names))

    def test_navigate_to_charity_details_page(self):
        """Functionalities 5: Navigate to Charity Details Page"""
        self.login("admin", "admin123")
        
        # Click on the first charity's details link
        details_link = self.driver.find_element(By.LINK_TEXT, 'Details')
        details_link.click()
        time.sleep(1)
        
        # Verify charity details page
        self.assertIn("Save the Children", self.driver.page_source)
        self.assertIn("Mission:", self.driver.page_source)
        self.assertIn("Projects:", self.driver.page_source)

    def test_view_contribution_history(self):
        """Functionalities 6: View Contribution History"""
        self.login("user1", "password1")
        
        # Check if donations are displayed
        donations = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertGreater(len(donations), 0)
        
        # Verify specific donation details
        donation_text = [d.text for d in donations]
        self.assertIn("50.00", " ".join(donation_text))
        self.assertIn("25.00", " ".join(donation_text))

    def test_donate_to_charity(self):
        """Functionalities 7: Donate to a Charity"""
        self.login("user1", "password1")
        
        # Navigate to charity details page
        details_link = self.driver.find_element(By.LINK_TEXT, 'Details')
        details_link.click()
        time.sleep(1)
        
        # Make a donation
        amount_field = self.driver.find_element(By.NAME, 'amount')
        amount_field.send_keys("10.50")
        self.driver.find_element(By.XPATH, '//button[text()="Donate"]').click()
        time.sleep(1)
        
        # Verify we're back on dashboard and donation appears
        self.assertIn("Dashboard", self.driver.title)
        donations = self.driver.find_elements(By.XPATH, '//ul/li')
        donation_text = [d.text for d in donations]
        self.assertIn("10.50", " ".join(donation_text))

    def test_user_logout(self):
        """Functionalities 8: User Logout"""
        self.login("admin", "admin123")
        
        # Click logout
        logout_link = self.driver.find_element(By.LINK_TEXT, 'Logout')
        logout_link.click()
        time.sleep(1)
        
        # Verify we're back on login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        """Functionalities 9: Navigate Back to Dashboard"""
        self.login("admin", "admin123")
        
        # Go to charity details
        details_link = self.driver.find_element(By.LINK_TEXT, 'Details')
        details_link.click()
        time.sleep(1)
        
        # Click back to dashboard
        back_link = self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard')
        back_link.click()
        time.sleep(1)
        
        # Verify we're back on dashboard
        self.assertIn("Dashboard", self.driver.title)
        charities = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertGreater(len(charities), 0)

    def test_local_data_storage(self):
        """Functionalities 10: Local Data Storage"""
        # This would require modifying the charities.txt file and verifying the changes
        # appear in the UI, which is not straightforward in automated tests
        # So we'll just verify the initial data is loaded correctly
        self.login("admin", "admin123")
        
        # Verify initial charities are loaded
        charities = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertEqual(len(charities), 3)  # Should match initial data

if __name__ == '__main__':
    unittest.main()
