import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Test user registration functionality
        self.driver.get('http://localhost:5000/register')
        time.sleep(1)

        new_username = "testuser"
        new_password = "testpassword"
        new_email = "testuser@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_login(self):
        # Test user login functionality
        self.login("user1", "password1")

        # Verify that the main page has loaded
        self.assertIn("Welcome to your Blog", self.driver.page_source)

    def test_create_new_post(self):
        # Test creating a new blog post
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        time.sleep(1)

        post_title = "New Blog Post"
        post_content = "This is the content of the new blog post."

        # Fill out the new post form
        self.driver.find_element(By.NAME, 'title').send_keys(post_title)
        self.driver.find_element(By.NAME, 'content').send_keys(post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()
        time.sleep(1)

        # Verify that the new post is displayed on the main page
        self.assertIn(post_title, self.driver.page_source)

    def test_view_blog_posts(self):
        # Test viewing blog posts after logging in
        self.login("user1", "password1")

        # Verify that the main page shows entries
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_post(self):
        # Test editing an existing post
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Edit Post').click()
        time.sleep(1)

        new_title = "Updated Blog Post"
        new_content = "This is the updated content of the blog post."

        # Fill out the edit post form
        self.driver.find_element(By.NAME, 'new_title').clear()
        self.driver.find_element(By.NAME, 'new_title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'new_content').clear()
        self.driver.find_element(By.NAME, 'new_content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Update Post"]').click()
        time.sleep(1)

        # Verify that the updated post is displayed on the main page
        self.assertIn(new_title, self.driver.page_source)

    def test_delete_post(self):
        # Test deleting an existing post
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Delete Post').click()
        time.sleep(1)

        # Verify that the post is no longer displayed on the main page
        self.assertNotIn("Updated Blog Post", self.driver.page_source)

    def test_logout(self):
        # Test logging out
        self.login("user1", "password1")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
