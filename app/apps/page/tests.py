from django.test import RequestFactory, TestCase
from django.test.client import WSGIRequest
from typing import Optional
from time import sleep
from .models import Page
from .services import increment_show_counter


class PageListTestCase(TestCase):
    def test_pages_smoke(self):
        response = self.client.get('/page/')
        self.assertEqual(response.status_code, 200)

    def test_pages_pagination(self):
        response = self.client.get('/page/')
        self.assertEqual(response.status_code, 200)

        response_json: dict = response.json()
        next_page_url: Optional[str] = response_json.get('next', None)
        self.assertIsNotNone(next_page_url)

        response = self.client.get(next_page_url)
        self.assertEqual(response.status_code, 200)


class PageDetailsTestCase(TestCase):
    def test_page_smoke(self):
        response = self.client.get('/page/')
        self.assertEqual(response.status_code, 200)

        response_json: dict = response.json()
        page_list: Optional[list] = response_json.get('results', None)
        self.assertIsNotNone(page_list)
        self.assertGreater(len(page_list), 0)

        first_page = page_list[0]
        page_url = first_page.get('url')
        response = self.client.get(page_url)
        self.assertEqual(response.status_code, 200)

    def test_page_increment_views_count(self):
        page = Page.objects.first()
        views_count = (
            page.content.values_list('views_count', flat=True).order_by().distinct().first()
        )
        increment_show_counter(page_id=page.pk)
        page = Page.objects.first()
        views_count_new = (
            page.content.values_list('views_count', flat=True).order_by().distinct().first()
        )
        self.assertEqual(views_count + 1, views_count_new)
