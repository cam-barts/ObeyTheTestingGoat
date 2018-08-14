# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse

# Create your models here.
class List(models.Model):
    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, on_delete=models.DO_NOTHING, default=None)

    class Meta:
        unique_together = ("list", "text")
