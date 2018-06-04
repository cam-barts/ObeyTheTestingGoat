from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import unittest
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
            self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    def test_can_start_a_list_and_retireve_it_later(self):
        # Open a browser to the web app
        self.browser.get(self.live_server_url)

        # "To-Do" in the title
        self.assertIn('To-Do', self.browser.title)

        # Header also mentions To-Do lists
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User inputs task
        inputbox.send_keys('Do something at sometime')
        # When user hits enter, the page updates
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Do something at sometime')

        #User inputs a different task
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do another thing at another time')
        inputbox.send_keys(Keys.ENTER)

        #Rows have both of the To-Do list items
        self.wait_for_row_in_list_table('1: Do something at sometime')
        self.wait_for_row_in_list_table('2: Do another thing at another time')

        self.fail('Finish the test')


if __name__ == '__main__':
    unittest.main(warnings=None)
