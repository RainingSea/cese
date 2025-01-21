import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestPersonalBlogApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8978/')  # Access the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionalities 1: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.NAME, 'email').send_keys('new_user@example.com')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

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
        self.driver.find_element(By.LINK_TEXT, 'New Post').click()

        self.driver.find_element(By.NAME, 'title').send_keys('Test Post')
        self.driver.find_element(By.NAME, 'content').send_keys('This is a test post content.')
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that the new post is displayed on the Main Blog Page
        self.assertIn('Test Post', self.driver.page_source)

    def test_view_blog_posts(self):
        # Functionalities 4: Test viewing blog posts
        self.login("admin", "admin123")

        # Verify that the Main Blog Page shows posts
        posts = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(posts), 0, "No blog posts found.")

    def test_edit_existing_post(self):
        # Functionalities 5: Test editing an existing post
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        self.driver.find_element(By.LINK_TEXT, 'Edit').click()

        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys('Updated First Post')
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys('Updated content of the first post.')
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()

        # Verify that the post is updated
        self.assertIn('Updated First Post', self.driver.page_source)

    def test_delete_blog_post(self):
        # Functionalities 6: Test deleting a blog post
        self.fail("Delete functionality is not implemented")

    def test_navigation(self):
        # Functionalities 7: Test navigation from View Post Page to Main Blog Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'First Post').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Main').click()

        # Verify that the user is returned to the Main Blog Page
        self.assertIn("Main Blog", self.driver.title)

    def test_user_logout(self):
        # Functionalities 8: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
