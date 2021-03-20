from celery import shared_task


@shared_task
def increment_show_counter_task(page_id: int) -> None:
    from .services import increment_show_counter

    increment_show_counter(page_id)
