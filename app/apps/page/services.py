from django.db.models import F
from .models import Page


def increment_show_counter(page_id: int) -> None:
    page: Page = Page.objects.get(pk=page_id)
    page.content.all().update(views_count=F('views_count') + 1)
