import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import sys
import io

class TestFreelancerMarketplace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the web application as a subprocess
        cls.process = subprocess.Popen(
            ['python', 'main.py'],
            stdout=subprocess.PIPE,  # Capture stdout of main.py
            stderr=subprocess.PIPE   # Capture stderr of main.py
        )
        time.sleep(2)  # Allow some time for the server to start

    @classmethod
    def tearDownClass(cls):
        # Terminate the subprocess
        cls.process.terminate()

        # Capture the output of main.py (both stdout and stderr)
        process_output, process_error = cls.process.communicate()

        # Decode and store the outputs for reporting
        cls.main_stdout = process_output.decode('utf-8') if process_output else ""
        cls.main_stderr = process_error.decode('utf-8') if process_error else ""


    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Welcome, admin", self.driver.page_source)
        # Capture the output of main.py (both stdout and stderr)
        process_output, process_error = self.process.communicate()

    # def test_navigate_to_registration(self):
    #     # Functionalities 2: Test navigation to the Registration Page
    #     self.driver.find_element(By.LINK_TEXT, 'Register').click()
    #
    #     # Verify that the Registration Page has loaded
    #     self.assertIn("Register", self.driver.title)
    #
    # def test_user_registration(self):
    #     # Functionalities 3: Test user registration functionality
    #     self.driver.find_element(By.LINK_TEXT, 'Register').click()
    #
    #     new_username = "new_user"
    #     new_password = "new_password"
    #
    #     # Input username and password for registration
    #     self.driver.find_element(By.NAME, 'username').send_keys(new_username)
    #     self.driver.find_element(By.NAME, 'password').send_keys(new_password)
    #     self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
    #     time.sleep(1)  # Wait for the next page to load
    #
    #     # Verify the user is redirected to the login page
    #     self.assertIn("Login", self.driver.title)
    #
    # def test_access_home_page_after_login(self):
    #     # Functionalities 4: Test accessing home page after login
    #     self.login("admin", "admin123")
    #
    #     # Verify that the Home Page has loaded
    #     self.assertIn("Welcome, admin", self.driver.page_source)
    #
    # def test_searching_for_freelancers(self):
    #     # Functionalities 5: Test searching for freelancers
    #     self.fail("Not implemented")
    #
    # def test_viewing_freelancer_profiles(self):
    #     # Functionalities 6: Test viewing freelancer profiles
    #     self.fail("Not implemented")
    #
    # def test_managing_projects(self):
    #     # Functionalities 7: Test managing projects
    #     self.login("admin", "admin123")
    #     self.driver.find_element(By.LINK_TEXT, 'Manage Projects').click()
    #     time.sleep(1)  # Wait for the next page to load
    #
    #     # Verify that the Project Management Page has loaded
    #     self.assertIn("Manage Projects", self.driver.page_source)
    #
    # def test_creating_new_project(self):
    #     # Functionalities 8: Test creating a new project
    #     self.fail("Not implemented")
    #
    # def test_viewing_project_lists(self):
    #     # Functionalities 9: Test viewing project lists
    #     self.fail("Not implemented")
    #
    # def test_profile_management(self):
    #     # Functionalities 10: Test profile management
    #     self.login("admin", "admin123")
    #     self.driver.find_element(By.LINK_TEXT, 'Profile Management').click()
    #     time.sleep(1)  # Wait for the next page to load
    #
    #     # Verify that the Profile Management Page has loaded
    #     self.assertIn("Edit Profile", self.driver.page_source)
    #
    # def test_updating_user_profile(self):
    #     # Functionalities 11: Test updating the user profile
    #     self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()

# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import subprocess
# import time
#
#
# class TestFreelancerMarketplace(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         try:
#             cls.process = subprocess.Popen(
#                 ['python', 'main.py'],
#                 stdout=subprocess.PIPE,  # Capture stdout of main.py
#                 stderr=subprocess.PIPE,  # Capture stderr of main.py
#                 text=True  # Decode output as text (string) instead of bytes
#             )
#             # Check for errors in stderr
#             stderr_output = cls.process.stderr.read()
#             if stderr_output:
#                 print("Error output from main.py:")
#                 print(stderr_output)
#                 cls.process.terminate()  # Terminate the process if there are errors
#
#     @classmethod
#     def tearDownClass(cls):
#         # Terminate the subprocess
#         cls.process.terminate()
#
#         # Capture the output of main.py (both stdout and stderr)
#         cls.main_stdout, cls.main_stderr = cls.process.communicate()
#         cls.main_stdout = cls.main_stdout.decode('utf-8') if cls.main_stdout else ""
#         cls.main_stderr = cls.main_stderr.decode('utf-8') if cls.main_stderr else ""
#
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.get('http://localhost:8299/')  # Open the login page
#
#     def tearDown(self):
#         self.driver.quit()
#
#     def login(self, username, password):
#         # Helper method to perform login
#         self.driver.find_element(By.NAME, 'username').send_keys(username)
#         self.driver.find_element(By.NAME, 'password').send_keys(password)
#         self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
#
#     def test_user_login(self):
#         """Test user login functionality."""
#         try:
#             self.login("admin", "admin123")
#             # Verify that the Home Page has loaded
#             self.assertIn("Welcome, admin", self.driver.page_source)
#         except Exception as e:
#             self.fail(f"Test failed due to an exception: {e}\n\n"
#                       f"--- main.py stdout ---\n{self.main_stdout}\n"
#                       f"--- main.py stderr ---\n{self.main_stderr}")
#
#
# if __name__ == '__main__':
#     unittest.main()
