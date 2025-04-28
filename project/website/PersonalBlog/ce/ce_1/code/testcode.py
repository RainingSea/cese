import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace 5000 with the actual port from main.py

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionalities 1: Test user registration functionality
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page
        self.driver.find_element(By.ID, 'username').send_keys("test_user")
        self.driver.find_element(By.ID, 'password').send_keys("test_password")
        self.driver.find_element(By.ID, 'email').send_keys("test@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the main blog page has loaded
        self.assertIn("Blog Posts", self.driver.title)

    def test_create_new_blog_post(self):
        # Functionalities 3: Test creating a new blog post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()

        self.driver.find_element(By.ID, 'title').send_keys("New Blog Post")
        self.driver.find_element(By.ID, 'content').send_keys("This is the content of the new blog post.")
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()

        # Verify that the new post is displayed on the main blog page
        self.assertIn("New Blog Post", self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: Test viewing blog posts after logging in
        self.login("admin", "admin123")

        # Verify that the main blog page shows existing posts
        self.assertIn("First Post", self.driver.page_source)
        self.assertIn("Second Post", self.driver.page_source)

    def test_edit_existing_post(self):
        # Functionalities 5: Test editing an existing post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Edit Post').click()

        self.driver.find_element(By.ID, 'new_title').send_keys("Updated Blog Post")
        self.driver.find_element(By.ID, 'new_content').send_keys("This is the updated content.")
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()

        # Verify that the post is updated
        self.assertIn("Updated Blog Post", self.driver.page_source)

    def test_delete_blog_post(self):
        # Functionalities 6: Test deleting a blog post
        self.login("admin", "admin123")
        # Assuming there's a delete button for the first post
        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()

        # Verify that the post is removed
        self.assertNotIn("First Post", self.driver.page_source)

    def test_navigate_back_to_main_blog(self):
        # Functionalities 7: Test navigation back to the main blog page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Post').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Blog').click()

        # Verify that the main blog page is displayed
        self.assertIn("Blog Posts", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
