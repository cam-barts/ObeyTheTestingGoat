# -*- coding: utf-8 -*-
import sys

from accounts.models import ListUser
from accounts.models import Token


class PasswordlessAuthenticationBackend(object):
    def authenticate(self, uid):
        print("uid", uid, file=sys.stderr)
        if not Token.objects.filter(uid=uid).exists():
            print("No Token Found", file=sys.stderr)
            return None
        token = Token.objects.get(uid=uid)
        try:
            user = ListUser.objects.get(email=token.email)
            print(f"Got User: {user}", file=sys.stderr)
            return user
        except ListUser.DoesNotExist:
            print("New User", file=sys.stderr)
            return ListUser.objects.create(email=token.email)

    def get_user(self, email):
        return ListUser.objects.get(email=email)
