# -*- coding: utf-8 -*-
from django.conf.urls import url

from accounts import views

urlpatterns = [url(r"^send_login_email", views.send_login_email)]
