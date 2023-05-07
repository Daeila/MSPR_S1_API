import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import secrets
from werkzeug.security import check_password_hash

from api_webshop import app
from db.db import get_db


class PageObject:
    URLs = {
        "auth": "http://localhost:5000/auth",
        "register": "http://localhost:5000/auth/register",
        "login": "http://localhost:5000/auth/login",
        "code": "http://localhost:5000/auth/key"
    }

    def __init__(self, driver_):
        self.driver = driver_
        self.login_ = PageObject.Login(driver_)
        self.register_ = PageObject.Register(driver_)

    def go_to_auth(self):
        url = self.URLs["auth"]
        self.driver.get(url)

    def go_to_register(self):
        url = self.URLs["register"]
        self.driver.get(url)

    def go_to_login(self):
        url = self.URLs["login"]
        self.driver.get(url)

    def go_to_code(self):
        url = self.URLs["key"]
        self.driver.get(url)

    def register_user(self, email, password):
        self.register_.get_email_field().set_email(email)
        self.register_.get_password_field().set_password(password)
        self.register_.register_user()

    def login_user(self, email, password):
        self.login_.get_email_field().set_email(email)
        self.login_.get_password_field().set_password(password)
        self.login_.log_user()

    class Login:
        def __init__(self, driver_):
            self.driver = driver_
            self.input_email = None
            self.input_password = None
            self.log_btn = None

        def get_email_field(self):
            self.input_email = self.driver.find_element(by=By.NAME, value="email")
            self.input_email.click()
            return self

        def get_password_field(self):
            self.input_password = self.driver.find_element(by=By.NAME, value="password")
            self.input_password.click()
            return self

        def set_email(self, email):
            self.input_email.send_keys(email)
            return self

        def set_password(self, password):
            self.input_password.send_keys(password)
            return self

        def log_user(self):
            self.log_btn = self.driver.find_element(by=By.ID, value="login_btn")
            self.log_btn.click()
            return self

    class Register:
        def __init__(self, driver_):
            self.driver = driver_
            self.input_email = None
            self.input_password = None
            self.input_user_type = None
            self.register_btn = None

        def get_email_field(self):
            self.input_email = self.driver.find_element(by=By.NAME, value="email")
            self.input_email.click()
            return self

        def get_password_field(self):
            self.input_password = self.driver.find_element(by=By.NAME, value="password")
            self.input_password.click()
            return self

        def get_user_type_field(self):
            self.input_user_type = self.driver.find_element(by=By.NAME, value="user_type")
            self.input_user_type.click()
            return self

        def set_email(self, email):
            self.input_email.send_keys(email)
            return self

        def set_password(self, password):
            self.input_password.send_keys(password)
            return self

        def set_user_type(self):
            return self

        def register_user(self):
            self.register_btn = self.driver.find_element(by=By.ID, value="register_btn")
            self.register_btn.click()
            return self


class TestAuthenticator(unittest.TestCase):
    driver = None
    email_webshop = secrets.token_urlsafe(10)
    password_webshop = "pwd"
    email_revendeur = secrets.token_urlsafe(10)
    password_revendeur = "pwd"

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            options=webdriver.EdgeOptions(),
        )
        cls.driver.maximize_window()
        cls.page = PageObject(cls.driver)
        with app.app_context():
            db = get_db()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_register_new_revender(self):
        self.page.go_to_register()
        self.page.register_user(self.email_revendeur, self.password_revendeur)
        with app.app_context():
            db = get_db()
            user = db.execute(
                "SELECT email, password, user_type FROM Users WHERE email = ?", (self.email_revendeur,)).fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user["user_type"], 1)
        self.assertTrue(check_password_hash(user["password"], self.password_revendeur))

    def test_register_new_webshop(self):
        self.page.go_to_register()
        self.page.register_user(self.email_revendeur, self.password_revendeur)
        with app.app_context():
            db = get_db()
            user = db.execute(
                "SELECT email, password, user_type FROM Users WHERE email = ?", (self.email_revendeur,)).fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user["user_type"], 2)
        self.assertTrue(check_password_hash(user["password"], self.password_revendeur))

    def test_login(self):
        self.page.go_to_login()
        self.page.login_user(self.email_revendeur, self.password_revendeur)
        self.assertEqual(self.driver.current_url, self.page.URLs["code"])


if __name__ == "__main__":
    TestAuthenticator()
