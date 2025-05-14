import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestTravelRecommenderApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8071/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('preferences'))

    def logout(self):
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.url_contains('login'))

    # Functionality 1: User Registration
    def test_user_registration(self):
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Test successful registration
        username = "test_user_" + str(int(time.time()))
        password = "test123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.url_contains('preferences'))
        
        # Test duplicate username registration
        self.logout()
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alert')))
        alert = self.driver.find_element(By.CLASS_NAME, 'alert')
        self.assertIn('Username already exists', alert.text)

    # Functionality 2: User Login
    def test_user_login(self):
        # Test successful login
        self.login("user1", "user123")
        self.assertIn('Travel Preferences', self.driver.page_source)
        self.logout()
        
        # Test invalid login
        self.driver.find_element(By.NAME, 'username').send_keys("invalid")
        self.driver.find_element(By.NAME, 'password').send_keys("invalid")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alert')))
        alert = self.driver.find_element(By.CLASS_NAME, 'alert')
        self.assertIn('Invalid username or password', alert.text)

    # Functionality 3: Input Travel Preferences
    def test_input_travel_preferences(self):
        self.login("user1", "user123")
        
        # Verify preferences form is displayed
        self.assertIn('Travel Preferences', self.driver.page_source)
        self.assertTrue(self.driver.find_element(By.NAME, 'budget').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'activities').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'climate').is_displayed())
        
        # Test submitting preferences
        budget_slider = self.driver.find_element(By.NAME, 'budget')
        self.driver.execute_script("arguments[0].value = '1200'; arguments[0].dispatchEvent(new Event('input'))", budget_slider)
        
        self.driver.find_element(By.ID, 'beach').click()
        self.driver.find_element(By.ID, 'hiking').click()
        
        climate_select = self.driver.find_element(By.NAME, 'climate')
        climate_select.find_element(By.XPATH, '//option[text()="Tropical"]').click()
        
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        self.wait.until(EC.title_contains('Recommended'))
        self.assertIn('Recommended Destinations', self.driver.page_source)

    # Functionality 4: Generate Travel Recommendations
    def test_generate_travel_recommendations(self):
        self.login("user1", "user123")
        
        # Navigate to recommendations page
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        self.wait.until(EC.title_contains('Recommended'))
        
        # Verify recommendations are displayed
        recommendations = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertGreater(len(recommendations), 0, "No recommendations found")
        
        # Verify destination details
        first_dest = recommendations[0]
        self.assertTrue(first_dest.find_element(By.CLASS_NAME, 'card-title').is_displayed())
        self.assertTrue(first_dest.find_element(By.CLASS_NAME, 'card-text').is_displayed())
        self.assertIn('Cost:', first_dest.text)
        self.assertIn('Climate:', first_dest.text)
        self.assertIn('Activities:', first_dest.text)

    # Functionality 5: Save Favorite Destinations
    def test_save_favorite_destinations(self):
        self.login("user1", "user123")
        
        # Navigate to recommendations page
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        self.wait.until(EC.title_contains('Recommended'))
        
        # Save a favorite
        first_save_button = self.driver.find_element(By.XPATH, '//a[contains(@href, "save_favorite")]')
        destination_name = first_save_button.get_attribute('href').split('/')[-1]
        first_save_button.click()
        
        # Verify we're still on recommendations page
        self.wait.until(EC.title_contains('Recommended'))
        
        # Note: The application doesn't have a favorites page to verify,
        # so we'll just verify the favorite was saved in the file
        with open('favorites.txt', 'r') as f:
            favorites = f.readlines()
        self.assertTrue(any(f"user1|{destination_name}" in line for line in favorites))

    # Functionality 6: User Logout
    def test_user_logout(self):
        self.login("user1", "user123")
        
        # Test logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Test accessing protected page after logout
        self.driver.get('http://localhost:8071/preferences')
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

    # Functionality 7: View Detailed Information About Destinations
    def test_view_destination_details(self):
        self.login("user1", "user123")
        
        # Navigate to recommendations page
        self.driver.find_element(By.XPATH, '//button[text()="Get Recommendations"]').click()
        self.wait.until(EC.title_contains('Recommended'))
        
        # Verify destination details are displayed
        recommendations = self.driver.find_elements(By.CLASS_NAME, 'card')
        for dest in recommendations:
            name = dest.find_element(By.CLASS_NAME, 'card-title').text
            description = dest.find_element(By.XPATH, './/p[contains(@class, "card-text")][1]').text
            cost = dest.find_element(By.XPATH, './/p[contains(., "Cost:")]').text
            climate = dest.find_element(By.XPATH, './/p[contains(., "Climate:")]').text
            activities = dest.find_element(By.XPATH, './/p[contains(., "Activities:")]').text
            
            self.assertTrue(name, "Destination name missing")
            self.assertTrue(description, "Description missing")
            self.assertIn('$', cost, "Cost format incorrect")
            self.assertTrue(climate.split(':')[1].strip(), "Climate missing")
            self.assertTrue(activities.split(':')[1].strip(), "Activities missing")

if __name__ == '__main__':
    unittest.main()
