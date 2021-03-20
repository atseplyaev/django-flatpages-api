from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import PageListSerializer, PageRetrieveSerializer
from .models import Page
from .tasks import increment_show_counter_task


class PageViewSet(ReadOnlyModelViewSet):
    queryset = Page.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PageRetrieveSerializer
        return PageListSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        instance: Page = self.get_object()
        increment_show_counter_task.delay(instance.pk)
        return response
