# -*- coding: utf-8 -*-
from unittest import skip

from django.utils.html import escape
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector(".has-error")

    def test_cannot_add_empty_item(self):
        # User Goes to site and accidentally submits an empty list item
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Home Page refreshes with Error indicating items cannot be blank
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )

        # User tries with some text and succeeds
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Do something at sometime")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("Do something at sometime")

        # User inputs a different task, also succeeding
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Do another thing at another time")
        inputbox.send_keys(Keys.ENTER)

        # Rows have both of the To-Do list items
        self.wait_for_row_in_list_table("Do something at sometime")
        self.wait_for_row_in_list_table("Do another thing at another time")

        # User attempts the empty list item again, just to make sure
        self.get_item_input_box().send_keys(Keys.ENTER)
        # Home Page refreshes with Error indicating items cannot be blank
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )

    def test_cannot_add_duplicate_item(self):
        # User goes to homepage and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("This is an Item")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1 This is an Item")

        # User attempts to duplicate the item
        self.get_item_input_box().send_keys("This is an Item")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # User recieves a helpful and well written error message
        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_element().text, escape(DUPLICATE_ITEM_ERROR)
            )
        )

    def test_error_messages_are_cleared_on_input(self):
        # User Generates a Validation error due to duplication
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Banter too thicc")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1 Banter too thicc")

        self.get_item_input_box().send_keys("Banter too thicc")
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))

        # User Begins Typing Again
        self.get_item_input_box().send_keys("a")

        # Error Message dissappears
        self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))
