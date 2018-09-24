# -*- coding: utf-8 -*-
from unittest.mock import patch

from django.test import TestCase

import accounts.views


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_list):
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        accounts.views.send_mail = fake_send_mail

        response = self.client.post(
            "/accounts/send_login_email", data={"email": "edith@example.com"}
        )
        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, "Your login link for Cam's To Do Lists")
        self.assertEqual(self.from_email, "noreply@CamsToDo")
        self.assertEqual(self.to_list, ["edith@example.com"])
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post(
            "/accounts/send_login_email", data={"email": "edith@example.com"}
        )

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link for Cam's To Do Lists")
        self.assertEqual(from_email, "noreply@CamsToDo")
        self.assertEqual(to_list, ["edith@example.com"])
