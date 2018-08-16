# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # User goes to home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # User notices input box is centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10
        )


if __name__ == "__main__":
    unittest.main(warnings=None)
