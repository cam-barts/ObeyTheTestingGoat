from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest
import time
import os

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

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

    def test_layout_and_styling(self):
        # User goes to home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # User notices input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

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

        # User inputs a different task
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do another thing at another time')
        inputbox.send_keys(Keys.ENTER)

        # Rows have both of the To-Do list items
        self.wait_for_row_in_list_table('1: Do something at sometime')
        self.wait_for_row_in_list_table('2: Do another thing at another time')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User 2 starts a new lists
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Something about peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Something about peacock feathers')

        # User 2 notices that her list has a unique url
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')

        # User 3 comes alongs
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # User 3 does not see user 2s list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Something about peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # User 3 starts a new grocery list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: milk')

        # User 3 gets own unique url
        user3_list_url = self.browser.current_url
        self.assertRegex(user3_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user3_list_url)

        # Ensure lists do not cross, and correct list shows
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Something about peacock feathers', page_text)
        self.assertIn('milk', page_text)


if __name__ == '__main__':
    unittest.main(warnings=None)
