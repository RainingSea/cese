import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the server and initialize the webdriver
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')  # Use the port from main.py

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionalities 1: Test user registration functionality
        self.driver.get('http://localhost:8000/register')  # Navigate to registration page
        time.sleep(1)

        new_username = "test_user"
        new_password = "test_password"
        new_email = "test@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_login(self):
        # Functionalities 2: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the main blog page has loaded
        self.assertIn("Blog Posts", self.driver.title)

    def test_create_new_post(self):
        # Functionalities 3: Test creating a new blog post
        self.login("admin", "admin123")

        # Navigate to New Post Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        time.sleep(1)

        post_title = "My New Post"
        post_content = "This is the content of my new post."

        # Fill out the new post form
        self.driver.find_element(By.NAME, 'title').send_keys(post_title)
        self.driver.find_element(By.NAME, 'content').send_keys(post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Post"]').click()
        time.sleep(1)

        # Verify that the new post is displayed on the main blog page
        self.assertIn(post_title, self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: Test viewing blog posts after logging in
        self.login("admin", "admin123")

        # Verify that the main blog page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming posts are in <li> elements
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_post(self):
        # Functionalities 5: Test editing an existing post
        self.login("admin", "admin123")

        # Navigate to the edit post page (assuming the first post is editable)
        self.driver.find_element(By.LINK_TEXT, 'Edit Post').click()
        time.sleep(1)

        new_title = "Updated Post Title"
        new_content = "Updated content for the post."

        # Fill out the edit post form
        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Changes"]').click()
        time.sleep(1)

        # Verify that the updated post is displayed
        self.assertIn(new_title, self.driver.page_source)

    def test_delete_post(self):
        # Functionalities 6: Test deleting a blog post
        self.login("admin", "admin123")

        # Navigate to the delete post page (assuming the first post is deletable)
        self.driver.find_element(By.LINK_TEXT, 'Delete Post').click()
        time.sleep(1)

        # Verify that the post is no longer displayed
        self.assertNotIn("Post Title", self.driver.page_source)  # Replace with actual post title

    def test_logout(self):
        # Functionalities 8: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
