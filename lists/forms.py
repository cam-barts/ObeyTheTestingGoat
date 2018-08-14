# -*- coding: utf-8 -*-
from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = "Oops! You Can't Have an Empty List Item!"


class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ("text",)
        widgets = {
            "text": forms.fields.TextInput(
                attrs={
                    "placeholder": "Enter a to-do item",
                    "class": "form-control input-lg",
                }
            )
        }
        error_messages = {"text": {"required": EMPTY_ITEM_ERROR}}
