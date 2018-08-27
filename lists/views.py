# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.html import escape

from lists.forms import EMPTY_ITEM_ERROR
from lists.forms import ExistingListItemForm
from lists.forms import ItemForm
from lists.models import Item
from lists.models import List


# Create your views here.
def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "list.html", {"list": list_, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form})
