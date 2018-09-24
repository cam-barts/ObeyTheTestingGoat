# -*- coding: utf-8 -*-
import re

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

TEST_EMAIL = "user@example.com"
SUBJECT = "Your login link for Cam's To Do Lists"


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # User navigates to login site and notices a Login in section in navbar
        # It invites user to log in via email address, which they do
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message notifys the user that an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                "check your email", self.browser.find_element_by_tag_name("body").text
            )
        )

        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a URL link in the email

        self.assertIn("Use this link to log in:", email.body)
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n {email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # User clicks the link
        self.browser.get(url)

        # User is logged in
        self.wait_for(lambda: self.browser.find_element_by_link_text("Log Out"))
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(TEST_EMAIL, navbar.text)
