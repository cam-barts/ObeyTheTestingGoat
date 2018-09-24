# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.shortcuts import redirect

# Create your views here.


def send_login_email(request):
    email = request.POST["email"]
    send_mail(
        "Your login link for Cam's To Do Lists",
        "Body Text",
        "noreply@CamsToDo",
        [email],
    )
    return redirect("/")
