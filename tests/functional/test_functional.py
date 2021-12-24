from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time


class TestPaths:
    expected_end_page = "GUDLFT Points Board"

    def test_should_connect_book_and_see_welcome_page(self, webdriver):
        """
        Gets to the Index page
        Fills email input (listed one)
        Clicks Enter / Gets to Welcome page
        Clicks on the link for current competition / Gets to Booking page
        Fill booking input for number of places to book: 1
        Clicks enter / Gets to Welcome page
        Clicks on logout link / Gets to Index Page
        Clicks on Club Point Board link / Gets to Club Points Board page

        There is sleep times between each action.

        Finally: checks if the title of the last page seen is the one expected
        """
        webdriver.get("http://127.0.0.1:5000/")
        input_email = webdriver.find_element(By.NAME, "email")
        input_email.send_keys("admin@irontemple.com")
        self.sleeping()
        input_email.send_keys(Keys.ENTER)
        compet = webdriver.find_element(By.TAG_NAME, "input")
        self.sleeping()
        compet.click()
        input_booking = webdriver.find_element(By.ID, "book_places")
        input_booking.send_keys("1")
        button_booking = webdriver.find_element(By.ID, "book_places")
        self.sleeping()
        button_booking.send_keys(Keys.ENTER)
        logout = webdriver.find_element(By.ID, "logout")
        self.sleeping()
        logout.click()
        points_board = webdriver.find_element(By.ID, "points_board")
        self.sleeping()
        points_board.click()
        self.sleeping()
        assert webdriver.title == self.expected_end_page

    def sleeping(self):
        return time.sleep(0)

    def tearDown(self, webdriver):
        if webdriver is not None:
            webdriver.close()
            webdriver.quit()
