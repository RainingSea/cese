import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow some time for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8107/')  # Access the login page

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

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input registration details
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify registration success message
        self.assertIn("Registration successful", self.driver.page_source)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "pass123")

        # Verify that the Main Blog Page has loaded
        self.assertIn("Main Blog Page", self.driver.page_source)

    def test_create_new_blog_post(self):
        # Test creating a new blog post
        self.login("admin", "pass123")

        # Navigate to New Post Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        time.sleep(1)  # Wait for the new post page to load

        post_title = "Test Post"
        post_content = "This is a test post."
        post_author = "admin"

        # Fill out the new post form
        self.driver.find_element(By.NAME, 'title').send_keys(post_title)
        self.driver.find_element(By.NAME, 'content').send_keys(post_content)
        self.driver.find_element(By.NAME, 'author').send_keys(post_author)
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()
        time.sleep(1)  # Wait for the post to be created

        # Verify success message
        self.assertIn("Post created successfully", self.driver.page_source)

    def test_view_blog_posts(self):
        # Test viewing blog posts after logging in
        self.login("admin", "pass123")

        # Verify that the Main Blog Page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Test editing an existing post
        self.login("admin", "pass123")

        # Navigate to a post and edit it
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the post page to load
        self.driver.find_element(By.LINK_TEXT, 'Edit Post').click()
        time.sleep(1)  # Wait for the edit page to load

        new_content = "Updated content for the first post."
        content_field = self.driver.find_element(By.NAME, 'content')
        content_field.clear()
        content_field.send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()
        time.sleep(1)  # Wait for the post to be updated

        # Verify success message
        self.assertIn("Post updated successfully", self.driver.page_source)

    def test_delete_blog_post(self):
        # Test deleting a blog post
        self.fail("Delete functionality not implemented")

    def test_navigation(self):
        # Test navigation from View Post Page to Main Blog Page
        self.login("admin", "pass123")

        # Navigate to a post and then back to main
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        time.sleep(1)  # Wait for the post page to load
        self.driver.find_element(By.LINK_TEXT, 'Back to Main').click()
        time.sleep(1)  # Wait for the main page to load

        # Verify that the Main Blog Page is displayed
        self.assertIn("Main Blog Page", self.driver.page_source)

    def test_user_logout(self):
        # Test logging out
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
