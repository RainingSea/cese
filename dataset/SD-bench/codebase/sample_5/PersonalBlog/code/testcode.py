import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8482/login')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Functionalities 1: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Main Blog Page has loaded
        self.assertIn("Main Blog", self.driver.title)

    def test_create_new_blog_post(self):
        # Functionalities 3: Test creating a new blog post
        self.login("admin", "admin123")

        # Navigate to New Post Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        time.sleep(1)  # Wait for the next page to load

        post_title = "My New Blog Post"
        post_content = "This is the content of my new blog post."

        # Fill out the new post form
        self.driver.find_element(By.NAME, 'title').send_keys(post_title)
        self.driver.find_element(By.NAME, 'content').send_keys(post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()
        time.sleep(1)  # Wait for the post to be created

        # Verify that the new post is displayed on the Main Blog Page
        self.assertIn(post_title, self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: Test viewing blog posts after logging in
        self.login("admin", "admin123")

        # Verify that the Main Blog Page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Functionalities 5: Test editing an existing post
        self.login("admin", "admin123")

        # Navigate to View Post Page
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the Edit button
        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        time.sleep(1)  # Wait for the edit page to load

        new_title = "Updated First Post"
        new_content = "This is the updated content of the first post."

        # Fill out the edit form
        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()
        time.sleep(1)  # Wait for the post to be updated

        # Verify that the updated post is displayed on the Main Blog Page
        self.assertIn(new_title, self.driver.page_source)

    def test_delete_blog_post(self):
        # Functionalities 6: Test deleting a blog post
        self.login("admin", "admin123")

        # Navigate to View Post Page
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the Delete button
        self.driver.find_element(By.LINK_TEXT, 'Delete').click()
        time.sleep(1)  # Wait for the post to be deleted

        # Verify that the post is no longer displayed on the Main Blog Page
        self.assertNotIn("First Post", self.driver.page_source)

    def test_navigation(self):
        # Functionalities 7: Test navigation from View Post Page to Main Blog Page
        self.login("admin", "admin123")

        # Navigate to View Post Page
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the Back to Main link
        self.driver.find_element(By.LINK_TEXT, 'Back to Main').click()
        time.sleep(1)  # Wait for the main page to load

        # Verify that the Main Blog Page is displayed
        self.assertIn("Main Blog", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
