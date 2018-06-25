from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_item(self):
        # User Goes to site and accidentally submits an empty list item
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # Home Page refreshes with Error indicating items cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "Oops! You Can't Have an Empty List Item!"
        ))

        # User tries with some text and succeeds
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do something at sometime')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Do something at sometime')

        # User inputs a different task, also succeeding
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do another thing at another time')
        inputbox.send_keys(Keys.ENTER)

        # Rows have both of the To-Do list items
        self.wait_for_row_in_list_table('1: Do something at sometime')
        self.wait_for_row_in_list_table('2: Do another thing at another time')

        # User attempts the empty list item again, just to make sure
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        # Home Page refreshes with Error indicating items cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "Oops! You Can't Have an Empty List Item!"
        ))




if __name__ == '__main__':
    unittest.main(warnings=None)
