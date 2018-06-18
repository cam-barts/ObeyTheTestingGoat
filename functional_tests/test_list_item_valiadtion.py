from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_item(self):
        self.fail("Write the test")



if __name__ == '__main__':
    unittest.main(warnings=None)
