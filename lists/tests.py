from django.test import TestCase
from django.urls import resolve
# from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items =Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) item')
        self.assertEqual(second_saved_item.text, 'Item the second')

class LiveViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client  .get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')


class NewLiveTest(TestCase):

    def test_can_save_a_POST_request(self):
        text = 'A new list item'
        self.client.post('/lists/new', data={'item_text': text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)

    def test_redirects_after_POST(self):
        text = 'A new list item'
        response = self.client.post('/lists/new', data={'item_text': text})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
