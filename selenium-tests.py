import unittest
from selenium import webdriver

class WebPageTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_web_page(self):
        driver = self.driver
        driver.get("http://127.0.0.1:4444/")
        self.assertIn("CIO Yard Sale", driver.title)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
