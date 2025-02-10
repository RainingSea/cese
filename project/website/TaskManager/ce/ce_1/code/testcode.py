import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os, time


class TestTaskManagerApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(
            ["python", "main.py"],
            cwd="D:/Project/CE/CE/project/website/TaskManager/ce/ce_1/code",
        )
        time.sleep(1)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8580/")

    def tearDown(self):
        # Close the web driver session and terminate the application process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        self.driver.find_element(By.NAME, "username").send_keys(new_username)
        self.driver.find_element(By.NAME, "password").send_keys(new_password)
        self.driver.find_element(By.NAME, "email").send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Create Account"]').click()

        self.assertIn("Login", self.driver.title)

    def test_view_task_list(self):
        # Functionalities 3: Test viewing task list
        self.login("admin", "admin123")
        tasks = self.driver.find_elements(By.TAG_NAME, "li")
        self.assertGreaterEqual(len(tasks), 0, "No tasks found.")

    def test_add_new_task(self):
        # Functionalities 4: Test adding a new task
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, "description").send_keys("New Task")
        self.driver.find_element(By.NAME, "due_date").send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()

        tasks = self.driver.find_elements(By.TAG_NAME, "li")
        self.assertTrue(
            any("New Task" in task.text for task in tasks), "Task not added."
        )

    def test_remove_task(self):
        # Functionalities 5: Test removing a task
        self.login("admin", "admin123")
        tasks_before = self.driver.find_elements(By.TAG_NAME, "li")
        if tasks_before:
            self.driver.find_element(By.LINK_TEXT, "Remove").click()
            tasks_after = self.driver.find_elements(By.TAG_NAME, "li")
            self.assertLess(len(tasks_after), len(tasks_before), "Task not removed.")
        else:
            self.fail("No tasks to remove.")

    def test_navigate_back_to_login(self):
        # Functionalities 6: Test navigating back to login
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        self.assertIn("Login", self.driver.title)

    def test_task_data_storage(self):
        # Functionalities 7: Test task data storage
        self.login("admin", "admin123")
        self.driver.find_element(By.NAME, "description").send_keys("Storage Task")
        self.driver.find_element(By.NAME, "due_date").send_keys("2023-12-31")
        self.driver.find_element(By.XPATH, '//button[text()="Add Task"]').click()

        with open("tasks_admin.txt", "r") as file:
            tasks = file.readlines()
            self.assertTrue(
                any("Storage Task" in task for task in tasks),
                "Task not stored in file.",
            )

        self.driver.find_element(By.LINK_TEXT, "Remove").click()
        with open("tasks_admin.txt", "r") as file:
            tasks = file.readlines()
            self.assertFalse(
                any("Storage Task" in task for task in tasks),
                "Task not removed from file.",
            )

    def test_invalid_actions(self):
        # Functionalities 8: Test invalid actions
        self.driver.get("http://localhost:8580/home")
        self.assertIn("Login", self.driver.title)

    def test_session_management(self):
        # Functionalities 9: Test session management
        self.login("admin", "admin123")
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8580/home")
        self.assertIn("Login", self.driver.title)


if __name__ == "__main__":
    unittest.main()
