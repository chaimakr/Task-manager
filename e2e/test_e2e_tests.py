from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from unittest import TestCase
import multiprocessing
from app import launch
import time 
from user_service import deleteUserTest
import os

#to run the test:
#coverage run -m unittest "e2e\test_e2e_tests.py"

class TaskManagerTest(TestCase):

    @classmethod
    def setUpClass(inst):
        inst.TaskManager_process=multiprocessing.Process(target=launch,name="TaskManager",args=('teste2e.db',True,))
        inst.TaskManager_process.start()
        time.sleep(1)
        inst.start = time.time()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-gpu')
        inst.driver = webdriver.Chrome(ChromeDriverManager().install())
        inst.driver.implicitly_wait(1)
        print("Visiting home page")
        inst.driver.get('http://localhost:5000/')
        inst.driver.save_screenshot('./e2e/screenshots/01homepage.png')


    def test_01_SignUp(self):
        print("Visiting Sign Up page")
        register_button = self.driver.find_element(by=By.ID, value='SignUp')
        register_button.click()
        self.driver.implicitly_wait(1)
        print("Filling Sign Up form")
        username_field = self.driver.find_element(by=By.ID, value='username')
        username_field.send_keys('e2e tester')
        self.driver.implicitly_wait(1)
        password_field = self.driver.find_element(by=By.ID, value='password')
        password_field.send_keys('0000')
        self.driver.implicitly_wait(1)
        self.driver.save_screenshot('./e2e/screenshots/02SignUppage.png')
        confirm_field = self.driver.find_element(by=By.ID, value='send')
        self.driver.implicitly_wait(1)
        confirm_field.click()
        print("Redirecting to login page")
        message = self.driver.find_element(by=By.ID, value='title_homepage').text
        expected_message = "Welcome to your Task Manager App"

        self.assertEqual(expected_message , message)

    def test_02_SignIn(self):
        print("Visiting Sign In page")
        register_button = self.driver.find_element(by=By.ID, value='SignIn')
        register_button.click()
        self.driver.implicitly_wait(1)
        print("Filling Sign Up form")
        username_field = self.driver.find_element(by=By.ID, value='usernamelogin')
        username_field.send_keys('root')
        self.driver.implicitly_wait(1)
        password_field = self.driver.find_element(by=By.ID, value='passwordlogin')
        password_field.send_keys('root')
        self.driver.implicitly_wait(1)
        confirm_field = self.driver.find_element(by=By.ID, value='sendlogin')
        self.driver.implicitly_wait(1)
        confirm_field.click()
        self.driver.save_screenshot('./e2e/screenshots/03TaskTable.png')
        print("Redirecting to Task manager table")
        message = self.driver.find_element(by=By.ID, value='title_homepage_user').text
        expected_message = "Hi"

        self.assertIn(expected_message , message)
        
    def test_03_addTask(self):
        print ("Adding a new task")
        add_button = self.driver.find_element(by=By.ID, value='addTask')
        task_field = self.driver.find_element(by=By.ID, value='task')
        self.driver.implicitly_wait(1)
        print("Filling task content")
        task_field.send_keys('e2e test task')
        self.driver.implicitly_wait(1)
        print("Saving task")
        add_button.click()
        self.driver.save_screenshot('./e2e/screenshots/04TaskAdded.png')
        message = self.driver.find_element(by=By.ID, value='title_homepage_user').text
        expected_message = "Hi"

        self.assertIn(expected_message , message)

    def test_04_updateStateTask(self):
        print ("Updating a task")
        update_button = self.driver.find_element(by=By.ID, value='updateStateTask')
        update_button.click()
        self.driver.save_screenshot('./e2e/screenshots/05TaskUpdated.png')
        message = self.driver.find_element(by=By.ID, value='title_homepage_user').text
        expected_message = "Hi"

        self.assertIn(expected_message , message)

    def test_05_deleteTask(self):
        print ("Deleting a task")
        delete_button = self.driver.find_element(by=By.ID, value='deleteTask')
        delete_button.click()
        self.driver.save_screenshot('./e2e/screenshots/06TaskDeleted.png')
        message = self.driver.find_element(by=By.ID, value='title_homepage_user').text
        expected_message = "Hi"

        self.assertIn(expected_message , message)

    def test_06_logout(self):
        print("Logging out")
        logout_button = self.driver.find_element(by=By.ID, value='logout')
        logout_button.click()
        self.driver.save_screenshot('./e2e/screenshots/07Logout.png')
        print("Redirecting to home page")
        message = self.driver.find_element(by=By.ID, value='title_homepage').text
        expected_message = "Welcome to your Task Manager App"

        self.assertEqual(expected_message , message)


    @classmethod
    def tearDownClass(inst):
        inst.end = time.time()
        elapsedtime=inst.end-inst.start
        print("\n-----------------------------------------------\n End 2 End test duration: ", "{:.2f}".format(elapsedtime), "seconds")
        inst.driver.quit()
        deleteUserTest("e2e tester")
        inst.TaskManager_process.terminate()
        os.remove('teste2e.db')
   