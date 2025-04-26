import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the server and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080/') 

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
        # Functionalities 1: User Registration
        self.driver.get('http://localhost:8080/register')  # Navigate to registration page
        time.sleep(1)

        new_username = "test_user"
        new_password = "test_password"
        new_email = "test@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_login(self):
        # Functionalities 2: User Login
        self.login("admin", "admin123")

        # Verify that the main blog page has loaded
        self.assertIn("Blog Posts", self.driver.title)

    def test_create_new_post(self):
        # Functionalities 3: Create a New Blog Post
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/new_post')  # Navigate to new post page
        time.sleep(1)

        post_title = "New Blog Post"
        post_content = "This is the content of the new blog post."

        # Fill out the new post form
        self.driver.find_element(By.NAME, 'title').send_keys(post_title)
        self.driver.find_element(By.NAME, 'content').send_keys(post_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for saving the post

        # Verify that the new post is displayed on the main blog page
        self.assertIn(post_title, self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: View Blog Posts
        self.login("admin", "admin123")

        # Verify that the main blog page shows posts
        self.assertIn("Blog Posts", self.driver.page_source)

    def test_edit_post(self):
        # Functionalities 5: Edit an Existing Post
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/edit_post')  # Navigate to edit post page
        time.sleep(1)

        new_content = "This is the updated content of the blog post."
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        time.sleep(1)  # Wait for saving the post

        # Verify that the post content has been updated
        self.assertIn(new_content, self.driver.page_source)

    def test_delete_post(self):
        # Functionalities 6: Delete a Blog Post
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/delete_post')  # Navigate to delete post page
        time.sleep(1)

        # Assuming there's a delete button for the post
        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()
        time.sleep(1)  # Wait for deletion

        # Verify that the post is no longer displayed
        self.assertNotIn("First Post", self.driver.page_source)

    def test_navigate_back(self):
        # Functionalities 7: Navigate back from the View Post Page to the Main Blog Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8080/view_post')  # Navigate to view post page
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, 'Back to Blog').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the main blog page is displayed
        self.assertIn("Blog Posts", self.driver.title)

    def test_logout(self):
        # Functionalities 8: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
