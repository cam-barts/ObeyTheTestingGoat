# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import DO_NOTHING
from django.urls import reverse

# Create your models here.
class List(models.Model):
    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=DO_NOTHING)

    class Meta:
        ordering = ("id",)
        unique_together = ("list", "text")

    def __str__(self):
        return self.text
